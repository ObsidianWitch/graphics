import bpy, bmesh

def bmesh2obj(bm, name):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    return bpy.data.objects.new(name, mesh)

def new_cube(*args, **kwargs):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, *args, **kwargs)
    obj = bmesh2obj(bm, name='Cube')
    bm.free()
    return obj
