import bpy, bmesh, dataclasses
from mathutils import Matrix, Vector

def delete_data():
    for data in (bpy.data.actions, bpy.data.cameras, bpy.data.lights,
                 bpy.data.materials, bpy.data.meshes, bpy.data.objects,
                 bpy.data.collections, bpy.data.images):
        for item in data:
            data.remove(item)

def new_obj(bmesh_op, name, *args, **kwargs):
    bm = bmesh.new()
    bmesh_op(bm, *args, **kwargs)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return bpy.data.objects.new(name, mesh)

@dataclasses.dataclass
class UVIsland:
    faces: list[bmesh.types.BMFace] = dataclasses.field(default_factory=list)
    bbox: tuple[float, 4] = None

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

def uv_cube_project(bm, margin=0.01):
    uv_layer = bm.loops.layers.uv[0]
    islands = { 'top':   UVIsland(), 'bottom': UVIsland(),
                'front': UVIsland(), 'back':   UVIsland(),
                'right': UVIsland(), 'left':   UVIsland() }

    # unwrap UVs using cube projection
    # note: faces loops produce split UVs, verts link_loops produce stitched UVs
    # ref: blender source uvedit_unwrap_cube_project() & axis_dominant_v3()
    for face in bm.faces:
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

    # position islands
    for island in islands.values():
        island.calc_bbox(uv_layer)

    for face in islands['front'].faces:
        for loop in face.loops:
            loop[uv_layer].uv.y -= islands['front'].bbox['b']

    for face in islands['top'].faces:
        for loop in face.loops:
            if islands['front'].faces:
                loop[uv_layer].uv.y += islands['front'].bbox['h'] + margin
            loop[uv_layer].uv.y -= islands['top'].bbox['b']

    for face in islands['bottom'].faces:
        for loop in face.loops:
            if islands['front'].faces:
                loop[uv_layer].uv.y += islands['front'].bbox['h'] + margin
            if islands['top'].faces:
                loop[uv_layer].uv.y += islands['top'].bbox['h'] + margin
            loop[uv_layer].uv.y -= islands['bottom'].bbox['b']

    for face in islands['right'].faces:
        for loop in face.loops:
            if islands['front'].faces:
                loop[uv_layer].uv.x += islands['front'].bbox['w'] + margin
            loop[uv_layer].uv.x -= islands['right'].bbox['l']
            loop[uv_layer].uv.y -= islands['right'].bbox['b']

    for face in islands['back'].faces:
        for loop in face.loops:
            if islands['front'].faces:
                loop[uv_layer].uv.x += islands['front'].bbox['w'] + margin
            if islands['right'].faces:
                loop[uv_layer].uv.x += islands['right'].bbox['w'] + margin
            loop[uv_layer].uv.x -= islands['back'].bbox['l']
            loop[uv_layer].uv.y -= islands['back'].bbox['b']

    for face in islands['left'].faces:
        for loop in face.loops:
            if islands['front'].faces:
                loop[uv_layer].uv.x += islands['front'].bbox['w'] + margin
            if islands['right'].faces:
                loop[uv_layer].uv.x += islands['right'].bbox['w'] + margin
            if islands['back'].faces:
                loop[uv_layer].uv.x += islands['back'].bbox['w'] + margin
            loop[uv_layer].uv.x -= islands['left'].bbox['l']
            loop[uv_layer].uv.y -= islands['left'].bbox['b']

    return islands
