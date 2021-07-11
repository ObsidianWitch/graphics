import bpy, bmesh

def new_mesh(bmesh_op, name, *args, **kwargs):
    bm = bmesh.new()
    bmesh_op(bm, *args, **kwargs)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)

def new_cube(*args, name='Cube', **kwargs):
    return new_mesh(bmesh.ops.create_cube, name, *args, **kwargs)

def shade(mesh, smooth):
    for p in mesh.polygons:
        p.use_smooth = smooth
