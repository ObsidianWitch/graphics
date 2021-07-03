#!/usr/bin/env -S blender --factory-startup --python

# name: Cube Owl
# blender: 2.93.0
# ref: https://www.youtube.com/watch?v=4xLdisAvjx8&list=PLa1F2ddGya_-UvuAqHAksYnB0qL9yWDO6&index=44

import sys
import bpy, bmesh
if "." not in sys.path: sys.path.append(".")
import addons.script_reset
import shared.mesh

class Owl:
    @classmethod
    def new(cls):
        collection = bpy.data.collections.new('Owl')
        torso = cls.new_torso()
        collection.objects.link(torso)
        return collection

    @classmethod
    def new_torso(cls):
        # object
        obj = shared.mesh.new_cube()
        obj.name = 'Torso'

        # modifiers
        obj.modifiers.new(name='Bevel', type='BEVEL')
        obj.modifiers['Bevel'].width = 0.02
        obj.modifiers['Bevel'].segments = 2

        return obj

if __name__ == '__main__':
    # reset data
    addons.script_reset.delete_data()

    # create character
    owl_collection = Owl.new()

    # setup scene
    scene = bpy.data.scenes[0]
    scene.collection.children.link(owl_collection)
