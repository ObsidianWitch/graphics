#!/usr/bin/env -S blender --factory-startup --python

# name: Cube Owl
# blender: 2.93.0
# ref: https://cloud.blender.org/training/primitive-animals/

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

        wings = cls.new_wings(anchor=torso)
        wings.parent = torso
        collection.objects.link(wings)

        return collection

    @classmethod
    def new_torso(cls):
        # mesh & object
        obj = shared.mesh.new_cube(name='Torso', size=2)
        shared.mesh.shade(obj.data, smooth=True)

        # modifiers
        bevel_mod = obj.modifiers.new(name='Bevel', type='BEVEL')
        bevel_mod.width = 0.02
        bevel_mod.segments = 2

        return obj

    @classmethod
    def new_wings(cls, anchor):
        # mesh
        # 1. manually place points to create rough wing outline
        # 2. select all vertices & create face
        # 3. poke faces
        # 4. offset central vertex
        mesh = bpy.data.meshes.new('Wing')
        mesh.from_pydata(
            vertices = ((0.00,  0.98, -0.63), (0.00, -0.18,  0.99),
                        (0.00, -0.91, -0.40), (0.00,  0.88, -0.63),
                        (0.00, -0.91,  0.64), (0.25, -0.09,  0.04),),
            edges = (),
            faces = ((1, 4, 5), (4, 2, 5), (2, 3, 5), (3, 0, 5), (0, 1, 5)),
        )
        shared.mesh.shade(mesh, smooth=True)

        # object
        obj = bpy.data.objects.new('Wings', mesh)
        obj.location.x = (obj.dimensions.x / 4) + anchor.location.x \
                       + (anchor.dimensions.x / 2)
        obj.location.z = -0.5
        obj.scale = (1.1, 1.1, 1.1)

        # modifiers
        subdiv_mod = obj.modifiers.new(name='Subdivision', type='SUBSURF')
        subdiv_mod.levels = subdiv_mod.render_levels = 2
        mirror1_mod = obj.modifiers.new(name='MirrorOrigin', type='MIRROR')
        mirror2_mod = obj.modifiers.new(name='MirrorObject', type='MIRROR')
        mirror2_mod.mirror_object = anchor
        bevel_mod = obj.modifiers.new(name='Bevel', type='BEVEL')

        return obj

if __name__ == '__main__':
    # reset data
    addons.script_reset.delete_data()

    # create character
    owl_collection = Owl.new()

    # setup scene
    scene = bpy.data.scenes[0]
    scene.collection.children.link(owl_collection)
