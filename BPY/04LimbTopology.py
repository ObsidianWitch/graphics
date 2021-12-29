#!/usr/bin/env -S blender --factory-startup --python

# blender: 3.0
# ref: http://wiki.polycount.com/wiki/Limb_Topology

import sys, importlib
from math import radians

import bpy, bmesh
from mathutils import Quaternion
C = bpy.context
D = bpy.data

if '.' not in sys.path:
    sys.path.append('.')
import shared
importlib.reload(shared)

def add_limb_naive() -> bpy.types.Object:
    # bmesh
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, segments=16, radius=0.1)
    c1 = { 'verts': bm.verts[:], 'edges': bm.edges[:], 'faces': bm.faces[:] }
    c2 = bmesh.ops.extrude_edge_only(bm, edges=c1['edges'])
    c2 = shared.bm_geom_split(c2['geom'])
    bmesh.ops.translate(bm, verts=c2['verts'], vec=(0, 0, 0.2))
    c3 = bmesh.ops.extrude_edge_only(bm, edges=c2['edges'])
    c3 = shared.bm_geom_split(c3['geom'])
    bmesh.ops.translate(bm, verts=c3['verts'], vec=(0, 0, 0.2))
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, -c2['verts'][0].co.z))

    # mesh & object
    mesh = D.meshes.new('limb_naive')
    object = D.objects.new(mesh.name, mesh)
    C.scene.collection.objects.link(object)

    # Vertex groups
    # ref: https://docs.blender.org/api/current/bmesh.html#customdata-access
    deform_layer = bm.verts.layers.deform.new()
    b1_vg = object.vertex_groups.new(name='limb.001')
    for vert in bm.verts[0:32]:
        vert[deform_layer][b1_vg.index] = 1.0
    b2_vg = object.vertex_groups.new(name='limb.002')
    for vert in bm.verts[16:48]:
        vert[deform_layer][b2_vg.index] = 1.0
    bm.to_mesh(mesh)
    bm.free()

    # Armature
    # ref: https://www.youtube.com/watch?v=cZ3o5tjO51s
    # ref: https://blender.stackexchange.com/a/51697
    armature = D.armatures.new('armature')
    armature = D.objects.new(armature.name, armature)
    armature.show_in_front = True
    C.scene.collection.objects.link(armature)

    C.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    bones = armature.data.edit_bones
    b1 = bones.new(b1_vg.name)
    b1.head = (0.0, 0.0, -0.3)
    b1.tail = (0.0, 0.0, 0.0)
    b2 = bones.new(b2_vg.name)
    b2.head = (0.0, 0.0, 0.0)
    b2.tail = (0.0, 0.0, 0.3)
    b2.parent = b1
    b2.use_connect = True
    bpy.ops.object.mode_set(mode='OBJECT')

    # Set armature as parent to object
    object.parent = armature
    modifier = object.modifiers.new(name='armature', type='ARMATURE')
    modifier.object = armature

    # Poses & keyframes
    pose_bones = armature.pose.bones
    pose_bones[b2_vg.name].keyframe_insert(data_path='rotation_quaternion', frame=1)
    pose_bones[b2_vg.name].keyframe_insert(data_path='rotation_quaternion', frame=100)
    pose_bones[b2_vg.name].rotation_quaternion = Quaternion((0, 0, 1), radians(-90))
    pose_bones[b2_vg.name].keyframe_insert(data_path='rotation_quaternion', frame=50)

    return armature

if __name__ == '__main__':
    shared.delete_data()
    C.scene.frame_current = 1
    C.scene.frame_end = 100
    add_limb_naive()
