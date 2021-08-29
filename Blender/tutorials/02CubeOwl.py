#!/usr/bin/env -S blender --factory-startup --python

# name: Cube Owl
# blender: 2.93.0
# ref: https://cloud.blender.org/training/primitive-animals/

import sys, math
import bpy, bmesh
from mathutils import Matrix, Vector
import numpy as np
if "." not in sys.path: sys.path.append(".")
import addons.script_reset
import shared.mesh

class Owl:
    @classmethod
    def new(cls):
        collection = bpy.data.collections.new('Owl')

        torso = cls.new_torso()
        collection.objects.link(torso)

        face_parts = cls.new_face()
        face_parts[0].parent = torso
        for part in face_parts:
            collection.objects.link(part)

        wings = cls.new_wings(anchor=torso)
        wings.parent = torso
        collection.objects.link(wings)

        feathers = cls.new_feathers(location=(0.0, 0.9, -0.6))
        for feather in feathers:
            feather.parent = torso
            collection.objects.link(feather)

        return collection

    @classmethod
    def new_torso(cls):
        # mesh & object
        obj = shared.mesh.new_cube(name='Torso', size=2)
        shared.mesh.shade(obj.data, smooth=True)

        # modifiers
        bevel_mod = obj.modifiers.new(name='Bevel', type='BEVEL')
        bevel_mod.width = 0.02
        bevel_mod.segments = 2

        return obj

    @classmethod
    def new_face(cls):
        base = cls.new_face_base()
        beak = cls.new_face_beak()
        beak.parent = base
        return [base, beak]


    @classmethod
    def new_face_base(cls):
        # mesh: half-heart face
        mesh = bpy.data.meshes.new('Face')
        mesh.from_pydata(
            # The vertices 1 and 5 control/guide the subdivision modifier.
            vertices=((0.0, 0.0, -0.72), (-0.045, 0, -0.702),
                      (-0.9, 0.0, -0.36), (-0.9, 0.0, 0.45),
                      (-0.45, 0.0, 0.9), (-0.040725, 0.0, 0.490725),
                      (0.0, 0.0, 0.45), (0.0, 0.0, -0.36)),
            edges=(),
            faces=((0, 1, 2, 7), (7, 2, 3, 6), (6, 3, 4, 5)),
        )
        shared.mesh.shade(mesh, smooth=True)

        # bmesh
        bm = bmesh.new()
        bm.from_mesh(mesh)

        # extrude
        bm.edges.ensure_lookup_table()
        _geom = bmesh.ops.extrude_face_region(bm,
            geom = bm.faces,
            # exclude these edges from the extrusion to avoid having inner
            # geometry creating a crease after the mirror modifier
            edges_exclude = set((bm.edges[3], bm.edges[8]))
        )
        bmesh.ops.translate(bm, vec=(0.0, -0.1, 0.0), verts=bm.verts[8:])

        bm.to_mesh(mesh)
        bm.free()

        # object
        obj = bpy.data.objects.new('Face', mesh)
        obj.location.y = -0.95
        mirror_mod = obj.modifiers.new(name='Mirror', type='MIRROR')
        subdiv_mod = obj.modifiers.new(name='Subdivision', type='SUBSURF')
        subdiv_mod.levels = subdiv_mod.render_levels = 2

        return obj

    @classmethod
    def new_face_beak(cls):
        def cartesian_circle(radius, angles):
            return tuple(zip(
                [0] * len(angles),
                radius * np.cos(angles),
                radius * np.sin(angles),
            ))

        def cartesian_log_spiral(a, k, angles):
            radius = a * np.exp(k * angles)
            return cartesian_circle(radius, angles)

        # Generate points on a circle and a logarithmic spiral for φ in
        # [start_angle;end_angle]. These two curves intersect at (r=1, φ=end_angle)
        # representing the extremity of the beak.
        def generate_vertices(start_angle=np.pi / 2, end_angle=np.pi, ncuts=4):
            cut_angles = np.linspace(start_angle, end_angle, ncuts)
            # add a cut near the beak extremity to control the subdivision
            cut_angles = np.insert(cut_angles, -1, [ cut_angles[-1] - 0.01 ])

            # circle
            r = 1
            outer_circle = cartesian_circle(r, cut_angles)

            # log spiral intersecting w/ previous circle at (r, end_angle)
            # circle_x(φ) = r*cos(φ)
            # spiral_x(φ) = a*exp(kφ)*cos(φ)
            # k = ln(r/a) / φ where a != r
            a = 0.05
            k = np.log(r / a) / end_angle
            inner_spiral = cartesian_log_spiral(a, k, cut_angles)

            return outer_circle, inner_spiral

        def generate_faces(curve1, curve2):
            assert(len(curve1) == len(curve2))
            faces = [ (i, i - 1, i + len(curve1) - 1, i + len(curve1))
                      for i in range(1, len(curve1) - 1) ]
            faces.append((len(curve1) - 1, len(curve1) - 2, 2 * len(curve1) - 2))
            return faces

        outer_circle, inner_spiral = generate_vertices()
        mesh = bpy.data.meshes.new('Beak')
        mesh.from_pydata(
            vertices = outer_circle + inner_spiral[:-1],
            edges = (),
            faces = generate_faces(outer_circle, inner_spiral),
        )
        shared.mesh.shade(mesh, smooth=True)

        obj = bpy.data.objects.new('Beak', mesh)
        set_origin(obj, inner_spiral[0] + (np.array(outer_circle[0]) - inner_spiral[0]) / 2)
        obj.location = (0, 0, 0)
        obj.scale = (0.45, 0.45, 0.45)

        return obj

    @classmethod
    def new_wings(cls, anchor):
        # mesh
        # 1. manually place points to create rough wing outline
        # 2. select all vertices & create face
        # 3. poke faces
        # 4. offset central vertex
        mesh = bpy.data.meshes.new('Wing')
        mesh.from_pydata(
            vertices = ((0.00,  0.98, -0.63), (0.00, -0.18,  0.99),
                        (0.00, -0.91, -0.40), (0.00,  0.88, -0.63),
                        (0.00, -0.91,  0.64), (0.25, -0.09,  0.04),),
            edges = (),
            faces = ((1, 4, 5), (4, 2, 5), (2, 3, 5), (3, 0, 5), (0, 1, 5)),
        )
        shared.mesh.shade(mesh, smooth=True)

        # object
        obj = bpy.data.objects.new('Wings', mesh)
        obj.location.x = (obj.dimensions.x / 4) + anchor.location.x \
                       + (anchor.dimensions.x / 2)
        obj.location.z = -0.5
        obj.scale = (1.1, 1.1, 1.1)

        # modifiers
        subdiv_mod = obj.modifiers.new(name='Subdivision', type='SUBSURF')
        subdiv_mod.levels = subdiv_mod.render_levels = 2
        mirror1_mod = obj.modifiers.new(name='MirrorOrigin', type='MIRROR')
        mirror2_mod = obj.modifiers.new(name='MirrorObject', type='MIRROR')
        mirror2_mod.mirror_object = anchor
        bevel_mod = obj.modifiers.new(name='Bevel', type='BEVEL')

        return obj

    @classmethod
    def new_feathers(cls, location):
        feathers = [ cls.new_feather() ]
        feathers[0].location = location
        feathers += [feathers[0].copy() for _ in range(4)]

        for feather, angle, scale in zip(
            feathers, range(-50, 75, 25), [0.6, 0.8, 1.0, 0.8, 0.6]
        ):
            feather.scale = (scale, scale, scale)
            feather.rotation_euler.z = math.radians(angle)
            # ref: https://blender.stackexchange.com/q/44760
            feather.rotation_euler = (
                Matrix.Rotation(math.radians(25), 3, 'X')
                @ feather.rotation_euler.to_matrix()
            ).to_euler()
        return feathers

    @classmethod
    def new_feather(cls):
        # mesh
        vertices = ((-0.27, 0.31, 0.0), (0.0, -0.88, 0.0),
                    (-0.27, 0.51, 0.0), (0.0, 0.90, 0.0),
                    (0.0, 0.40, 0.10), (-0.10, 0.90, 0.0),
                    (-0.05, -0.88, 0.0))
        faces = ((3, 5, 4), (5, 2, 4), (0, 4, 2), (1, 4, 0, 6))
        mesh = bpy.data.meshes.new('Feather')
        mesh.from_pydata(vertices=vertices, edges=(), faces=faces)
        shared.mesh.shade(mesh, smooth=True)

        # object
        obj = bpy.data.objects.new('Feather', mesh)

        # modifiers
        mirrorx_mod = obj.modifiers.new(name='MirrorX', type='MIRROR')
        mirrorx_mod.use_clip = True
        subdiv_mod = obj.modifiers.new(name='Subdivision', type='SUBSURF')
        subdiv_mod.levels = subdiv_mod.render_levels = 2
        mirrorz_mod = obj.modifiers.new(name='MirrorZ', type='MIRROR')
        mirrorz_mod.use_axis = (False, False, True)

        # origin
        set_origin(obj, vertices[1])

        return obj

# ref: https://blender.stackexchange.com/a/35830
def set_origin(object, point):
    point = Vector(point)
    object.data.transform(Matrix.Translation(-point))
    object.matrix_world.translation += point

if __name__ == '__main__':
    # reset data
    addons.script_reset.delete_data()

    # create character
    owl_collection = Owl.new()

    # setup scene
    scene = bpy.data.scenes[0]
    scene.collection.children.link(owl_collection)
