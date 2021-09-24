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

def bm_geom_split(geom):
    return {
        'geom': geom,
        'verts': tuple(e for e in geom if isinstance(e, bmesh.types.BMVert)),
        'edges': tuple(e for e in geom if isinstance(e, bmesh.types.BMEdge)),
        'faces': tuple(e for e in geom if isinstance(e, bmesh.types.BMFace)),
    }

def obj_apply_transforms(obj):
    obj.data.transform(obj.matrix_basis)
    obj.matrix_basis.identity()

# note: Object.evaluated_get(evaluated_depsgraph) is an alternative but it
# requires the object being linked to a collection, which is inconvenient.
def obj_evaluate(obj, remove_src=False):
    bm = bmesh.new()
    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    mesh_eval = bpy.data.meshes.new(obj.data.name)
    bm.to_mesh(mesh_eval)
    obj_eval = bpy.data.objects.new(obj.name, mesh_eval)
    bm.free()
    if remove_src:
        bpy.data.meshes.remove(obj.data) # removes both the mesh and object
    return obj_eval

# ref: https://blender.stackexchange.com/a/133024
def obj_join(sources, remove_src=False):
    assert all(type(obj) == bpy.types.Object for obj in sources)

    ctx = {}
    ctx["selected_objects"] = ctx["selected_editable_objects"] = sources
    ctx["object"] = ctx["active_object"] = sources[0]
    bpy.ops.object.join(ctx)
    if remove_src:
        for src in sources[1:]:
            bpy.data.meshes.remove(src.data) # removes both the mesh and object
    return sources[0]
