#!/usr/bin/env -S blender --factory-startup --python

# ref: [CG Cookie - Animating With Python](https://www.youtube.com/watch?v=QnvN1dieIAU)
# ref: [BPY Documentation](https://docs.blender.org/api/current/)
# ref: [Python Performance with Blender operators](https://blender.stackexchange.com/a/7360)
# blender version: 2.92.0

import bpy, itertools

bpy.context.preferences.view.show_splash = False
for data_type in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                  bpy.data.meshes, bpy.data.objects, bpy.data.collections):
    for item in data_type: data_type.remove(item)

# 10*10 cubes grid
bpy.ops.mesh.primitive_cube_add()
cubetpl = bpy.context.active_object
cubetpl.modifiers.new(name='Wireframe', type='WIREFRAME')
cubetpl.modifiers['Wireframe'].thickness = 0.05
for x, y in itertools.product(range(10), repeat=2):
    if x == 0 and y == 0: continue
    c = cubetpl.copy()
    c.location[0] = x * 2
    c.location[1] = y * 2
    bpy.data.scenes['Scene'].collection.objects.link(c)

# animation
bpy.data.scenes['Scene'].frame_end = 80 + len(bpy.data.objects)
for i, obj in enumerate(bpy.data.objects):
    obj.scale = (0, 0, 0)
    obj.keyframe_insert(data_path='scale', frame=1 + i)
    obj.scale = (1, 1, 5)
    obj.keyframe_insert(data_path='scale', frame=50 + i)
    obj.scale = (1, 1, 0.5)
    obj.keyframe_insert(data_path='scale', frame=70 + i)
    obj.scale = (1, 1, 1)
    obj.keyframe_insert(data_path='scale', frame=80 + i)
