#!/usr/bin/env -S blender --factory-startup --python

# ref: [CG Cookie - Animating With Python](https://www.youtube.com/watch?v=QnvN1dieIAU)
# blender version: 2.92.0

import bpy

bpy.context.preferences.view.show_splash = False
for data_type in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                  bpy.data.meshes, bpy.data.objects, bpy.data.collections):
    for item in data_type: data_type.remove(item)

# cubes collection
cubes_collection = bpy.data.collections.new('cubes')
bpy.context.scene.collection.children.link(cubes_collection)
view_layer = bpy.context.view_layer
view_layer.active_layer_collection = view_layer.layer_collection.children[cubes_collection.name]

# 10*10 cubes grid
bpy.ops.mesh.primitive_cube_add()
for _ in range(9):
    bpy.ops.object.duplicate(linked=True)
    bpy.ops.transform.translate(value=(0, 2, 0))
bpy.ops.object.select_all(action='SELECT')
for _ in range(9):
    bpy.ops.object.duplicate(linked=True)
    bpy.ops.transform.translate(value=(2, 0, 0))

# animation
bpy.data.scenes['Scene'].frame_end = 80 + len(cubes_collection.objects)
for i, obj in enumerate(cubes_collection.objects):
    obj.scale = (0, 0, 0)
    obj.keyframe_insert(data_path='scale', frame=1 + i)
    obj.scale = (1, 1, 5)
    obj.keyframe_insert(data_path='scale', frame=50 + i)
    obj.scale = (1, 1, 0.5)
    obj.keyframe_insert(data_path='scale', frame=70 + i)
    obj.scale = (1, 1, 1)
    obj.keyframe_insert(data_path='scale', frame=80 + i)
