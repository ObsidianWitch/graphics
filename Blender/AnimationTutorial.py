#!/usr/bin/env -S blender --factory-startup --python

# ref: [CG Cookie - Animating With Python](https://www.youtube.com/watch?v=QnvN1dieIAU)

import bpy

bpy.context.preferences.view.show_splash = False
for data_type in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                  bpy.data.meshes, bpy.data.objects, bpy.data.collections):
    for item in data_type: data_type.remove(item)

# 10*10 cubes grid
bpy.ops.mesh.primitive_cube_add(size=2)
for _ in range(9):
    bpy.ops.object.duplicate(linked=True)
    bpy.ops.transform.translate(value=(0, 2, 0))
bpy.ops.object.select_all(action='SELECT')
for _ in range(9):
    bpy.ops.object.duplicate(linked=True)
    bpy.ops.transform.translate(value=(2, 0, 0))
