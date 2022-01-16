#!/usr/bin/env -S blender --factory-startup --python

# blender: 3.0
# ref: https://danbooru.donmai.us/posts/4519692
# ref: https://danbooru.donmai.us/posts/4116403

import sys, importlib
from math import radians
from pathlib import Path

import bpy, bmesh
from mathutils import Matrix, Vector
C = bpy.context
D = bpy.data
def Mat(*args): return Matrix(args)
def Vec(*args): return Vector(args)

if '.' not in sys.path:
    sys.path.append('.')
import shared
importlib.reload(shared)

class Character:
    @classmethod
    def object(cls):
        # bmesh
        bm = bmesh.new()
        shared.bm_absorb_obj(bm, cls.torso())

        # mesh & object
        mesh = D.meshes.new('character')
        bm.to_mesh(mesh)
        bm.free()
        object = D.objects.new(mesh.name, mesh)
        return object

    @classmethod
    def torso(cls) -> bpy.types.Object:
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()

        l1 = { 'v': shared.bm_create_plane(bm, fill=True)['verts'] }
        bmesh.ops.scale(bm, verts=l1['v'], vec=(1.2, 0.2, 1.0))
        bmesh.ops.translate(bm, verts=l1['v'], vec=(0.0, 0.0, 2.0))

        l2 = { 'v': shared.bm_create_plane(bm, fill=False)['verts'] }
        bmesh.ops.scale(bm, verts=l2['v'], vec=(1.1, 0.6, 1.0))
        bmesh.ops.translate(bm, verts=l2['v'], vec=(0.0, 0.0, 1.2))

        l3 = { 'v': shared.bm_create_plane(bm, fill=False)['verts'] }
        bmesh.ops.scale(bm, verts=l3['v'], vec=(0.5, 0.4, 1.0))
        bmesh.ops.translate(bm, verts=l3['v'], vec=(0.0, -0.2, 0.0))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)

        # mesh & object
        mesh = D.meshes.new('torso')
        bm.to_mesh(mesh)
        bm.free()
        object = D.objects.new(mesh.name, mesh)
        return object

if __name__ == '__main__':
    shared.delete_data()
    D.scenes[0].collection.objects.link(Character.object())
