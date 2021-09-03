import bpy, bmesh
from mathutils import Matrix, Vector

def delete_data():
    for data in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                 bpy.data.materials, bpy.data.meshes, bpy.data.objects,
                 bpy.data.collections):
        for item in data:
            data.remove(item)

def new_obj(bmesh_op, name, *args, **kwargs):
    bm = bmesh.new()
    bmesh_op(bm, *args, **kwargs)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)

def use_smooth(mesh, value):
    for p in mesh.polygons:
        p.use_smooth = value

# ref: https://blender.stackexchange.com/a/35830
def set_origin(object, point):
    point = Vector(point)
    object.data.transform(Matrix.Translation(-point))
    object.matrix_world.translation += point
