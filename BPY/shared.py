import bpy, bmesh, dataclasses
from mathutils import Matrix, Vector

def delete_data():
    for prop_collection in (
        bpy.data.actions, bpy.data.armatures, bpy.data.cameras,
        bpy.data.lights, bpy.data.materials, bpy.data.meshes,
        bpy.data.objects, bpy.data.collections, bpy.data.images
    ):
        for item in prop_collection:
            prop_collection.remove(item)

def setup_reference(blendpath, type='Collection', name='References'):
    bpy.ops.wm.append(filepath=f"{filepath}/{type}/{name}",
                      directory=f"{filepath}/{type}",
                      filename=name)
    for obj in bpy.data.collections['References'].objects:
        obj.hide_viewport = True
        obj.show_in_front = True
        obj.display_type = 'WIRE'

def new_obj(bmesh_op, name, *args, **kwargs):
    bm = bmesh.new()
    bmesh_op(bm, *args, **kwargs)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)

def bm_geom_split(geom):
    return {
        'geom': geom,
        'verts': tuple(e for e in geom if isinstance(e, bmesh.types.BMVert)),
        'edges': tuple(e for e in geom if isinstance(e, bmesh.types.BMEdge)),
        'faces': tuple(e for e in geom if isinstance(e, bmesh.types.BMFace)),
    }

@dataclasses.dataclass
class UVIsland:
    faces: list[bmesh.types.BMFace] = dataclasses.field(default_factory=list)
    bbox: dict[str, float] = None

    def calc_bbox(self, uv_layer) -> tuple[float, 4]:
        if not self.faces: return None
        top = bottom = left = right = None
        for face in self.faces:
            for loop in face.loops:
                uv = loop[uv_layer].uv
                top = uv.y if top is None else max(top, uv.y)
                left = uv.x if left is None else min(left, uv.x)
                right = uv.x if right is None else max(right, uv.x)
                bottom = uv.y if bottom is None else min(bottom, uv.y)
        self.bbox = { 't': top, 'l': left, 'r': right, 'b': bottom,
                      'h': top - bottom, 'w': right - left }
        return self.bbox

# Unwrap UVs using cube projection.
def bm_uv_cube_project(faces, uv_layer):
    islands = { 'top':   UVIsland(), 'bottom': UVIsland(),
                'front': UVIsland(), 'back':   UVIsland(),
                'right': UVIsland(), 'left':   UVIsland() }

    # unwrap UVs using cube projection
    # note: faces loops produce split UVs, verts link_loops produce stitched UVs
    # ref: blender source uvedit_unwrap_cube_project() & axis_dominant_v3()
    for face in faces:
        n = face.normal
        # pick the 2 non-dominant axes for the projection
        if abs(n.z) >= abs(n.x) and abs(n.z) >= abs(n.y):
            i, j = 0, 1
            islands['top' if n.z >= 0 else 'bottom'].faces.append(face)
        elif abs(n.y) >= abs(n.x) and abs(n.y) >= abs(n.z):
            i, j = 0, 2
            islands['back' if n.y >= 0 else 'front'].faces.append(face)
        else:
            i, j = 1, 2
            islands['right' if n.x >= 0 else 'left'].faces.append(face)

        for loop in face.loops:
            loop[uv_layer].uv.x = loop.vert.co[i]
            loop[uv_layer].uv.y = loop.vert.co[j]

    # islands' bounding boxes
    for island in islands.values():
        island.calc_bbox(uv_layer)

    return islands

# Position islands resulting from a cube projection.
def bm_uv_cube_position(islands, uv_layer, init_offset=Vector((0.5, 0.0)), margin=0.01):
    # position islands at (0, 0), offset them and update the bbox
    def do_position(key, offset):
        for face in islands[key].faces:
            for loop in face.loops:
                loop[uv_layer].uv.x += offset.x - islands[key].bbox['l']
                loop[uv_layer].uv.y += offset.y - islands[key].bbox['b']
        islands[key].calc_bbox(uv_layer)

    # select which axis of the specified island will contribute to the offset
    def do_offset(key, offset, axis):
        if islands[key].faces:
            offset.x += axis[0] * (islands[key].bbox['w'] + margin)
            offset.y += axis[1] * (islands[key].bbox['h'] + margin)

    # place front, top and bottom islands on the same row
    offset = init_offset.copy()
    do_position('front', offset)
    do_offset('front', offset, axis=(0, 1))
    do_position('top', offset)
    do_offset('top', offset, axis=(0, 1))
    do_position('bottom', offset)

    # place right, back and left islands on the same column as the front island
    offset = init_offset.copy()
    do_offset('front', offset, axis=(1, 0))
    do_position('right', offset)
    do_offset('right', offset, axis=(1, 0))
    do_position('back', offset)
    do_offset('back', offset, axis=(1, 0))
    do_position('left', offset)
