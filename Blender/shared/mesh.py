import bpy, bmesh

def new_cube(*args, name='Cube', **kwargs):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, *args, **kwargs)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)

def shade(mesh, smooth):
    for p in mesh.polygons:
        p.use_smooth = smooth
