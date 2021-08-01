#!/usr/bin/env -S blender --factory-startup --python

# name: Cube Owl
# blender: 2.93.0
# ref: https://cloud.blender.org/training/primitive-animals/

import sys, math
import bpy, bmesh
from mathutils import Matrix, Vector
if "." not in sys.path: sys.path.append(".")
import addons.script_reset
import shared.mesh

class Owl:
    @classmethod
    def new(cls):
        collection = bpy.data.collections.new('Owl')

        torso = cls.new_torso()
        collection.objects.link(torso)

        wings = cls.new_wings(anchor=torso)
        wings.parent = torso
        collection.objects.link(wings)

        feather = cls.new_feather()
        feather.location = (0.0, 0.9, -0.6)
        feather.rotation_euler.x = math.radians(25)
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
    def new_feather(cls):
        # mesh
        mesh = bpy.data.meshes.new('Feather')
        mesh.from_pydata(
            vertices = ((-0.27, 0.31, 0.0), (0.0, -0.88, 0.0),
                        (-0.27, 0.51, 0.0), (0.0, 0.90, 0.0),
                        (0.0, 0.40, 0.10), (-0.10, 0.90, 0.0),
                        (-0.05, -0.88, 0.0)),
            edges = (),
            faces = ((3, 5, 4), (5, 2, 4), (0, 4, 2), (1, 4, 0, 6)),
        )
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
        set_origin(obj, (0.0, -0.88, 0.0))

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
