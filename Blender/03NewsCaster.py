#!/usr/bin/env -S blender --factory-startup --python

# blender: 2.93
# ref: Mega Man Legends News Caster

import sys, math
import bpy, bmesh
from mathutils import Matrix
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

class Character:
    @classmethod
    def list(cls):
        return [cls.torso(), cls.legs()]

    @classmethod
    def torso(cls):
        bm = bmesh.new()

        luppertop = create_plane(bm, fill=False)
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

        mesh = bpy.data.meshes.new('torso')
        bm.to_mesh(mesh)
        bm.free()
        return bpy.data.objects.new('torso', mesh)

    @classmethod
    def legs(cls):
        bm = bmesh.new()
        ltop = create_plane(bm, fill=False)
        bmesh.ops.scale(bm, verts=ltop['verts'], vec=(0.16, 0.16, 1.0))
        bmesh.ops.scale(bm, verts=ltop['verts'][1::2], vec=(1.0, 1.15, 1.0))
        bmesh.ops.translate(bm, verts=ltop['verts'], vec=(0.0794, 0.016, 0.83))
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

        object = bpy.data.objects.new('legs', mesh)
        object.modifiers.new(name='mirror', type='MIRROR')
        return object

def setup_reference():
    bpy.ops.wm.append(filepath="03Reference.blend/Collection/References",
                      directory="03Reference.blend/Collection",
                      filename="References")
    references = bpy.data.collections['References'].objects
    for obj in references:
        obj.hide_viewport = True
        obj.show_in_front = True
        obj.display_type = 'WIRE'
    references['torso'].hide_viewport = False

def setup_scene():
    scene = bpy.data.scenes[0]
    for part in Character.list():
        scene.collection.objects.link(part)

if __name__ == '__main__':
    shared.delete_data()
    setup_reference()
    setup_scene()
