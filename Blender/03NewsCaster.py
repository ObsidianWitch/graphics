#!/usr/bin/env -S blender --factory-startup --python

# blender: 2.93
# ref: Mega Man Legends News Caster

import sys, math
import bpy, bmesh
from mathutils import Matrix, Vector
Diagonal = Matrix.Diagonal
Rotation = Matrix.Rotation
Translation = Matrix.Translation

if '.' not in sys.path:
    sys.path.append('.')
if 'shared' in sys.modules:
    del sys.modules['shared']
import shared

def create_plane(bm, fill):
    result = bmesh.ops.create_grid(bm, x_segments=0, y_segments=0, size=0.5)
    if not fill:
        bmesh.ops.delete(bm, geom=result['verts'][0].link_faces, context='FACES_ONLY')
    return result

def bm_absorb_obj(bm, obj):
    bm.from_mesh(obj.data)
    bpy.data.meshes.remove(obj.data) # removes both the mesh and object from bpy.data

class Character:
    def __init__(self, name='Character'):
        cls = self.__class__

        # mesh & object
        bm = bmesh.new()

        ## create pelvis from torso and legs
        bm_absorb_obj(bm, cls.torso())
        bm_absorb_obj(bm, cls.legs())
        bmesh.ops.bridge_loops(bm, edges=bm.edges[6:8] + bm.edges[17:18] + bm.edges[25:29])
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[55:57], cuts=1)
        bm.verts.ensure_lookup_table()
        bm.verts[32].co = bm.verts[19].co
        bm.verts[33].co.y = bm.verts[19].co.y
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0001)

        ## add remaining parts
        bm_absorb_obj(bm, cls.head())
        bm_absorb_obj(bm, cls.arms())
        bmesh.ops.mirror(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
            merge_dist=0.001, axis='X')
        bm_absorb_obj(bm, cls.nose())
        bm_absorb_obj(bm, cls.neck())

        self.obj = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        bm.to_mesh(self.obj.data)
        bm.free()

        # material
        self.obj.data.materials.append(cls.material())

    @classmethod
    def head(cls):
        bm = bmesh.new()

        sphv = bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=5,
            diameter=0.5)['verts']
        bmesh.ops.scale(bm, verts=sphv, vec=(0.36, 0.37, 0.35))
        bmesh.ops.translate(bm, verts=sphv, vec=(0.0, 0.03, 1.53))
        bmesh.ops.bisect_plane(bm, geom=sphv, dist=0.0000001, plane_co=(0, 0, 0),
            plane_no=(1, 0, 0), clear_inner=True)
        sphv = bm.verts[:]

        # tweak right
        sphv[16].co.z -= 0.01
        sphv[11].co.y -= 0.02
        bmesh.ops.translate(bm, verts=sphv[1:14:4], vec=(0.0, 0.0, -0.03))
        sphv[13].co.y += 0.015
        sphv[1].co.y -= 0.04
        sphv[14].co.y -= 0.01
        sphv[15].co.z = sphv[14].co.z
        bmesh.ops.rotate(bm, cent=sphv[15].co, verts=sphv[2:15:4] + sphv[15:16],
            matrix=Rotation(math.radians(10), 4, 'X'))
        bmesh.ops.scale(bm, verts=sphv[7:11], vec=(1.0, 0.0, 1.0))
        bmesh.ops.translate(bm, verts=sphv[7:11], vec=(0.0, -0.08, 0.0))
        sphv[10].co.z += 0.015

        # tweak front
        sphv[9].co.x -= 0.045
        sphv[5].co.x = sphv[9].co.x
        sphv[10].co.x -= 0.035

        # hair back spike
        pokev = bmesh.ops.poke(bm, faces=sphv[2].link_faces[0:1])['verts']
        pokev[0].co += Vector((-pokev[0].co.x, 0.06, -0.09))
        bmesh.ops.pointmerge(bm, verts=(pokev[0], sphv[2]), merge_co=pokev[0].co)

        mesh = bpy.data.meshes.new('head')
        bm.to_mesh(mesh)
        bm.free()

        return bpy.data.objects.new(mesh.name, mesh)

    @classmethod
    def nose(cls):
        bm = bmesh.new()
        conev = bmesh.ops.create_cone(bm, segments=3, diameter1=1.0,
            diameter2=0.0, depth=1.0)['verts']
        bmesh.ops.rotate(bm, verts=conev, matrix=Rotation(math.radians(90), 3, 'X'))
        bmesh.ops.scale(bm, verts=conev, vec=(0.02, 0.04, 0.04))
        bmesh.ops.translate(bm, verts=conev, vec=(0.0, -0.122, 1.443))
        conev[0].co.y -= 0.01

        mesh = bpy.data.meshes.new('nose')
        bm.to_mesh(mesh)
        bm.free()

        return bpy.data.objects.new(mesh.name, mesh)

    @classmethod
    def neck(cls):
        bm = bmesh.new()

        lneck1 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=lneck1['verts'], vec=(0.07, 0.06, 1.0))
        bmesh.ops.scale(bm, verts=lneck1['verts'][2:], vec=(0.0, 1.07, 1.0))
        bmesh.ops.translate(bm, verts=lneck1['verts'], vec=(0.0, 0.02, 1.35))

        bmesh.ops.extrude_edge_only(bm, edges=bm.edges)
        bmesh.ops.translate(bm, verts=bm.verts[-4:], vec=(0.0, 0.0, 0.07))

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

        mesh = bpy.data.meshes.new('neck')
        bm.to_mesh(mesh)
        bm.free()

        return bpy.data.objects.new(mesh.name, mesh)

    @classmethod
    def torso(cls):
        bm = bmesh.new()

        luppertop = create_plane(bm, fill=True)
        bmesh.ops.scale(bm, verts=luppertop['verts'], vec=(0.14, 0.1, 1.0))
        bmesh.ops.translate(bm, verts=luppertop['verts'], vec=(0.0, 0.015, 1.352))

        luppermid = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=luppermid['verts'], vec=(0.24, 0.18, 1.0))
        bmesh.ops.translate(bm, verts=luppermid['verts'], vec=(0.0, -0.017, 1.21))

        lwaist = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=lwaist['verts'], vec=(0.14, 0.11, 1.0))
        bmesh.ops.translate(bm, verts=lwaist['verts'], vec=(0.0, -0.02, 1.076))

        lbot = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=lbot['verts'], vec=(0.23, 0.16, 1.0))
        bmesh.ops.translate(bm, verts=lbot['verts'], vec=(0.0, -0.004, 0.999))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
            dist=0.0000001, plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True)

        mesh = bpy.data.meshes.new('torso')
        bm.to_mesh(mesh)
        bm.free()

        return bpy.data.objects.new(mesh.name, mesh)

    @classmethod
    def arms(cls):
        bm = bmesh.new()

        l1 = create_plane(bm, fill=True)
        bmesh.ops.scale(bm, verts=l1['verts'], vec=(0.11, 0.07, 1.0))
        bmesh.ops.rotate(bm, verts=l1['verts'], cent=l1['verts'][0].co,
                         matrix=Rotation(math.radians(10), 4, 'Y'))

        l2 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=l2['verts'], vec=(0.14, 0.07, 1.0))
        bmesh.ops.translate(bm, verts=l2['verts'], vec=l1['verts'][0].co - l2['verts'][0].co)
        bmesh.ops.rotate(bm, verts=l2['verts'], cent=l1['verts'][0].co,
                         matrix=Rotation(math.radians(15), 4, 'Y'))

        l3 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=l3['verts'], vec=(0.16, 0.07, 1.0))
        bmesh.ops.translate(bm, verts=l3['verts'], vec=l1['verts'][0].co - l3['verts'][0].co)
        bmesh.ops.rotate(bm, verts=l3['verts'], cent=l1['verts'][0].co,
                         matrix=Rotation(math.radians(35), 4, 'Y'))

        bmesh.ops.translate(bm, verts=bm.verts, vec=(0.12627, 0.019375, 1.3378))

        l4 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=l4['verts'], vec=(0.07, 0.06, 1.0))
        bmesh.ops.rotate(bm, verts=l4['verts'],
                         matrix=Rotation(math.radians(-10), 4, 'Y'))
        bmesh.ops.translate(bm, verts=l4['verts'], vec=(0.20385, 0.02, 1.0928))

        l5 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=l5['verts'], vec=(0.08, 0.06, 1.0))
        bmesh.ops.rotate(bm, verts=l5['verts'],
                         matrix=Rotation(math.radians(-12), 4, 'Y'))
        bmesh.ops.translate(bm, verts=l5['verts'], vec=(0.24261, 0.02, 0.94141))

        l6 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=l6['verts'], vec=(0.13, 0.15, 1.0))
        bmesh.ops.translate(bm, verts=l6['verts'], vec=(0.25, 0.0, 0.81))
        bmesh.ops.translate(bm, verts=l6['verts'][1::1], vec=(0.0, 0.0, -0.01))
        bmesh.ops.translate(bm, verts=l6['verts'][2:3], vec=(0.03, 0.0, 0.0))

        l7 = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=l7['verts'], vec=(0.0, 0.12, 1.0))
        bmesh.ops.translate(bm, verts=l7['verts'], vec=(0.22202, 0.01375, 0.75588))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

        mesh = bpy.data.meshes.new('arms')
        bm.to_mesh(mesh)
        bm.free()

        return bpy.data.objects.new(mesh.name, mesh)

    @classmethod
    def legs(cls):
        bm = bmesh.new()
        ltop = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=ltop['verts'], vec=(0.16, 0.16, 1.0))
        bmesh.ops.scale(bm, verts=ltop['verts'][1::2], vec=(1.0, 1.15, 1.0))
        bmesh.ops.translate(bm, verts=ltop['verts'], vec=(0.08, 0.016, 0.83))
        bmesh.ops.translate(bm, verts=ltop['verts'][1::2], vec=(0.0, 0.0, 0.084))

        lmid = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=lmid['verts'], vec=(0.1, 0.1, 1.0))
        bmesh.ops.translate(bm, verts=lmid['verts'], vec=(0.065, 0.025, 0.55))

        lbot = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=lbot['verts'], vec=(0.1, 0.1, 1.0))
        bmesh.ops.translate(bm, verts=lbot['verts'], vec=(0.06566, 0.033125, 0.0))
        bmesh.ops.translate(bm, verts=lbot['verts'][0:2], vec=(0.0, 0.0, 0.15))

        lfeet = create_plane(bm, fill=True)
        bmesh.ops.scale(bm, verts=lfeet['verts'], vec=(0.1, 0.06, 1.0))
        bmesh.ops.translate(bm, verts=lfeet['verts'], vec=(0.06625, -0.178+0.03, 0.0))
        bmesh.ops.rotate(bm, verts=lfeet['verts'], cent=lfeet['verts'][0].co,
                         matrix=Rotation(math.radians(80), 4, 'X'))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)

        mesh = bpy.data.meshes.new('legs')
        bm.to_mesh(mesh)
        bm.free()

        return bpy.data.objects.new(mesh.name, mesh)

    @classmethod
    def material(cls):
        material = bpy.data.materials.new(name='Material')
        material.use_nodes = True

        nodes = material.node_tree.nodes
        nodes['Principled BSDF'].inputs['Specular'].default_value = 0.0

        return material

def import_from_blend(filepath, type, name):
    bpy.ops.wm.append(filepath  = f"{filepath}/{type}/{name}",
                      directory = f"{filepath}/{type}",
                      filename  = name)

def setup_reference():
    import_from_blend('03Reference.blend', 'Collection', 'References')
    references = bpy.data.collections['References'].objects
    for obj in references:
        obj.hide_viewport = False
        obj.show_in_front = True
        obj.display_type = 'WIRE'

def setup_scene():
    scene = bpy.data.scenes[0]
    scene.collection.objects.link(Character().obj)

if __name__ == '__main__':
    shared.delete_data()
    setup_scene()
