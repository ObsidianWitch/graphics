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

def setup_scene():
    scene = bpy.data.scenes[0]
    for part in Character.list():
        scene.collection.objects.link(part)

if __name__ == '__main__':
    shared.delete_data()
    setup_scene()
