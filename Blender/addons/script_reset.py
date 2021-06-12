import sys, bpy
from pathlib import Path

bl_info = {
    "name": "Script Reset",
    "author": "Obsidienne",
    "blender": (2, 80, 0),
    "category": "Development",
}
keymaps = []

# Delete cached modules imported from the current directory.
def delete_modules():
    for f in Path('.').glob('**/*.py'):
        if str(f) == '.': continue
        module = str(f.with_suffix('')) \
            .removesuffix('/__init__') \
            .replace('/', '.')
        if module in sys.modules:
            del sys.modules[module]

def delete_data():
    for data in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                 bpy.data.materials, bpy.data.meshes, bpy.data.objects,
                 bpy.data.collections):
        for item in data:
            data.remove(item)

class ScriptResetRun(bpy.types.Operator):
    bl_idname = 'text.reset_run'
    bl_label = 'Reset and run script'
    def execute(self, context):
        bpy.ops.text.reload()
        delete_modules()
        delete_data()
        bpy.ops.text.run_script()
        return {"FINISHED"}

def register():
    # add operators
    bpy.utils.register_class(ScriptResetRun)

    # add keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Text', space_type='TEXT_EDITOR')
    kmi = km.keymap_items.new('text.reset_run', 'P', 'PRESS', alt=True)
    keymaps.append((km, kmi))

def unregister():
    # remove operators
    bpy.utils.unregister_class(ScriptResetRun)

    # remove keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

if __name__ == "__main__":
    register()
