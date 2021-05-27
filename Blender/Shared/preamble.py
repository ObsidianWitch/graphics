import bpy

def delete_data():
    for data_type in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                      bpy.data.materials, bpy.data.meshes, bpy.data.objects,
                      bpy.data.collections):
        for item in data_type:
            data_type.remove(item)

def reset():
    bpy.context.preferences.view.show_splash = False
    delete_data()
