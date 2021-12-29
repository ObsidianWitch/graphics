#!/usr/bin/env -S blender --factory-startup --python

# blender: 3.0
# ref: http://wiki.polycount.com/wiki/Limb_Topology

import sys, importlib
from math import radians

import bpy, bmesh
from mathutils import Matrix, Quaternion
C = bpy.context
D = bpy.data

if '.' not in sys.path:
    sys.path.append('.')
import shared
importlib.reload(shared)

def add_limb_one_loop() -> bpy.types.Object:
    # bmesh
    bm = bmesh.new()
    bm_cylinder_zcuts(bm, segments=16, radius=0.1, zcuts=(0.2, 0.2))

    # mesh & object
    mesh = D.meshes.new('limb_one_loop')
    object = D.objects.new(mesh.name, mesh)
    C.scene.collection.objects.link(object)

    # vertex groups
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

    # armature
    return add_limb_armature(object, b1_vg.name, b2_vg.name)

def add_limb_two_loops() -> bpy.types.Object:
    # bmesh
    bm = bmesh.new()
    bm_cylinder_zcuts(bm, segments=16, radius=0.1, zcuts=(0.19, 0.01, 0.2))

    # mesh & object
    mesh = D.meshes.new('limb_two_loops')
    object = D.objects.new(mesh.name, mesh)
    C.scene.collection.objects.link(object)

    # vertex groups
    # ref: https://docs.blender.org/api/current/bmesh.html#customdata-access
    deform_layer = bm.verts.layers.deform.new()
    b1_vg = object.vertex_groups.new(name='limb.001')
    for vert in bm.verts[0:32]:
        vert[deform_layer][b1_vg.index] = 1.0
    b2_vg = object.vertex_groups.new(name='limb.002')
    for vert in bm.verts[32:]:
        vert[deform_layer][b2_vg.index] = 1.0
    bm.to_mesh(mesh)
    bm.free()

    # armature
    return add_limb_armature(object, b1_vg.name, b2_vg.name)

def add_limb_one_triangle() -> bpy.types.Object:
    # bmesh
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, segments=16, radius=0.1)
    c1 = { 'verts': bm.verts[:], 'edges': bm.edges[:], 'faces': bm.faces[:] }
    c2 = bmesh.ops.extrude_edge_only(bm, edges=c1['edges'])
    c2 = shared.bm_geom_split(c2['geom'])
    bmesh.ops.translate(bm, verts=c2['verts'], vec=(0, 0, 0.2))
    bmesh.ops.transform(bm,
        verts=c2['verts'][9:],
        matrix=Matrix.Shear('YZ', 4, (0.0, -1.0))
    )
    c3 = bmesh.ops.extrude_edge_only(bm, edges=c2['edges'][8:])
    c3 = shared.bm_geom_split(c3['geom'])
    bmesh.ops.transform(bm,
        verts=c3['verts'],
        matrix=Matrix.Shear('YZ', 4, (0.0, 2.0))
    )
    c4 = bmesh.ops.extrude_edge_only(bm, edges=c2['edges'][0:8] + c3['edges'])
    c4 = shared.bm_geom_split(c4['geom'])
    bmesh.ops.translate(bm, verts=c4['verts'], vec=(0, 0, 0.2))
    bmesh.ops.transform(bm,
        verts=c4['verts'][9:],
        matrix=Matrix.Shear('YZ', 4, (0.0, -1.0))
    )
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    # mesh & object
    mesh = D.meshes.new('limb_one_triangle')
    object = D.objects.new(mesh.name, mesh)
    C.scene.collection.objects.link(object)

    # vertex groups
    # ref: https://docs.blender.org/api/current/bmesh.html#customdata-access
    deform_layer = bm.verts.layers.deform.new()
    b1_vg = object.vertex_groups.new(name='limb.001')
    for vert in bm.verts[0:32]:
        vert[deform_layer][b1_vg.index] = 1.0
    b2_vg = object.vertex_groups.new(name='limb.002')
    for vert in bm.verts[16:24] + bm.verts[31:]:
        vert[deform_layer][b2_vg.index] = 1.0
    bm.to_mesh(mesh)
    bm.free()

    # armature
    return add_limb_armature(object, b1_vg.name, b2_vg.name)

def bm_cylinder_zcuts(bm, zcuts, **kwargs):
    bmesh.ops.create_circle(bm, **kwargs)
    c_old = { 'verts': bm.verts[:], 'edges': bm.edges[:], 'faces': bm.faces[:] }
    for z in zcuts:
        c_new = bmesh.ops.extrude_edge_only(bm, edges=c_old['edges'])
        c_new = shared.bm_geom_split(c_new['geom'])
        bmesh.ops.translate(bm, verts=c_new['verts'], vec=(0, 0, z))
        c_old = c_new

# ref: https://www.youtube.com/watch?v=cZ3o5tjO51s
# ref: https://blender.stackexchange.com/a/51697
def add_limb_armature(object, b1_name, b2_name):
    # armature
    armature = D.armatures.new('armature')
    armature = D.objects.new(armature.name, armature)
    armature.show_in_front = True
    C.scene.collection.objects.link(armature)

    C.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    bones = armature.data.edit_bones
    b1 = bones.new(b1_name)
    b1.head = (0.0, 0.0, 0.0)
    b1.tail = (0.0, 0.0, 0.2)
    b2 = bones.new(b2_name)
    b2.head = (0.0, 0.0, 0.0)
    b2.tail = (0.0, 0.0, 0.4)
    b2.parent = b1
    b2.use_connect = True
    bpy.ops.object.mode_set(mode='OBJECT')

    # set armature as parent to object
    object.parent = armature
    modifier = object.modifiers.new(name='armature', type='ARMATURE')
    modifier.object = armature

    # set poses & keyframes
    pose_bones = armature.pose.bones
    pose_bones[b2_name].keyframe_insert(data_path='rotation_quaternion', frame=1)
    pose_bones[b2_name].keyframe_insert(data_path='rotation_quaternion', frame=100)
    pose_bones[b2_name].rotation_quaternion = Quaternion((0, 0, 1), radians(-90))
    pose_bones[b2_name].keyframe_insert(data_path='rotation_quaternion', frame=50)

    return armature

if __name__ == '__main__':
    shared.delete_data()
    C.scene.frame_current = 1
    C.scene.frame_end = 100
    limb1 = add_limb_one_loop()
    limb2 = add_limb_two_loops()
    limb2.location.x += 0.4
    limb3 = add_limb_one_triangle()
    limb3.location.x += 0.8
