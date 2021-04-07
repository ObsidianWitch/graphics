#!/usr/bin/env -S blender --factory-startup --python

# ref: [CG Cookie - Animating With Python](https://www.youtube.com/watch?v=QnvN1dieIAU)

import bpy

bpy.context.preferences.view.show_splash = False
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 10*10 cubes grid
bpy.ops.mesh.primitive_cube_add(size=2)
for _ in range(9):
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(0, 2, 0)})
bpy.ops.object.select_all(action='SELECT')
for _ in range(9):
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(2, 0, 0)})

