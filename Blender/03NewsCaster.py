#!/usr/bin/env -S blender --factory-startup --python

# blender: 2.93
# ref: Mega Man Legends News Caster

import sys
import bpy

if '.' not in sys.path:
    sys.path.append('.')
if 'shared' in sys.modules:
    del sys.modules['shared']
import shared

class Character:
    @classmethod
    def list(cls):
        return []

def setup_reference():
    bpy.ops.wm.append(filepath="03Reference.blend/Collection/References",
                      directory="03Reference.blend/Collection",
                      filename="References")
    references = bpy.data.collections['References'].objects
    for obj in references:
        obj.hide_viewport = True
        obj.show_in_front = True
        obj.display_type = 'WIRE'
    references['leg'].hide_viewport = False

def setup_scene():
    scene = bpy.data.scenes[0]
    for part in Character.list():
        scene.collection.objects.link(part)

if __name__ == '__main__':
    shared.delete_data()
    setup_reference()
    setup_scene()
