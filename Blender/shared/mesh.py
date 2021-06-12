import bpy, bmesh

def new_cube(*args, **kwargs):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, *args, **kwargs)
    mesh = bpy.data.meshes.new('Cube')
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new('Cube', mesh)
    return obj
