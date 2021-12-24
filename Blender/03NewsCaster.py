#!/usr/bin/env -S blender --factory-startup --python

# blender: 3.0
# ref: Mega Man Legends News Caster

import sys, importlib
from math import radians
from pathlib import Path

import bpy, bmesh
from mathutils import Matrix, Vector
C = bpy.context
D = bpy.data
def Mat(*args): return Matrix(args)
def Vec(*args): return Vector(args)
Diagonal = Matrix.Diagonal
Rotation = Matrix.Rotation
Translation = Matrix.Translation

import PIL.Image, PIL.ImageDraw # https://pypi.org/project/Pillow/

if '.' not in sys.path:
    sys.path.append('.')
import shared
importlib.reload(shared)

def create_plane(bm, fill):
    result = bmesh.ops.create_grid(bm, x_segments=0, y_segments=0, size=0.5)
    if not fill:
        bmesh.ops.delete(bm, geom=result['verts'][0].link_faces,
                         context='FACES_ONLY')
    return result

def bm_absorb_obj(bm, obj):
    bm.from_mesh(obj.data)
    for m in obj.data.materials:
        D.materials.remove(m)
    D.meshes.remove(obj.data) # removes both the mesh and object from bpy.data

class Character:
    @classmethod
    def object(cls):
        # mesh & object
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()
        bm_absorb_obj(bm, cls.head())
        bm_absorb_obj(bm, cls.arm())
        bm_absorb_obj(bm, cls.pelvis())
        bmesh.ops.mirror(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                         merge_dist=0.001, axis='X', mirror_u=True)
        bm_absorb_obj(bm, cls.nose())
        bm_absorb_obj(bm, cls.neck())

        mesh = D.meshes.new('character')
        bm.to_mesh(mesh)
        bm.free()
        object = D.objects.new(mesh.name, mesh)

        # texture & material
        texture = cls.texture()
        material = cls.material(texture)
        object.data.materials.append(material)

        return object

    @classmethod
    def scale_uvs(cls, faces, uv_layer, islands={}):
        for face in faces:
            for loop in face.loops:
                loop[uv_layer].uv.x -= 0.5
                loop[uv_layer].uv *= 0.27
                loop[uv_layer].uv.x += 0.5
        for island in islands.values():
            island.calc_bbox(uv_layer)

    @classmethod
    def head(cls) -> bpy.types.Object:
        bm = bmesh.new()

        uv_layer = bm.loops.layers.uv.new()
        sphv = bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=5,
                                         radius=0.5)['verts']
        bmesh.ops.scale(bm, verts=sphv, vec=(0.36, 0.37, 0.35))
        bmesh.ops.translate(bm, verts=sphv, vec=(0.0, 0.03, 1.53))
        bmesh.ops.bisect_plane(bm, geom=sphv, dist=0.0000001, plane_co=(0, 0, 0),
                               plane_no=(1, 0, 0), clear_inner=True)
        sphv = bm.verts[:]

        # tweak right
        sphv[16].co.z -= 0.01
        sphv[11].co.y -= 0.02
        bmesh.ops.translate(bm, verts=sphv[1:14:4], vec=(0.0, 0.0, -0.03))
        sphv[13].co.y += 0.015
        sphv[1].co.y -= 0.04
        sphv[14].co.y -= 0.01
        sphv[15].co.z = sphv[14].co.z
        bmesh.ops.rotate(bm, cent=sphv[15].co, verts=sphv[2:15:4] + sphv[15:16],
                         matrix=Rotation(radians(10), 4, 'X'))
        bmesh.ops.scale(bm, verts=sphv[7:11], vec=(1.0, 0.0, 1.0))
        bmesh.ops.translate(bm, verts=sphv[7:11], vec=(0.0, -0.08, 0.0))
        sphv[10].co.z += 0.015

        # tweak front
        sphv[9].co.x -= 0.045
        sphv[5].co.x = sphv[9].co.x
        sphv[10].co.x -= 0.035

        # hair back spike
        pokev = bmesh.ops.poke(bm, faces=sphv[2].link_faces[0:1])['verts']
        pokev[0].co += Vec(-pokev[0].co.x, 0.06, -0.09)
        bmesh.ops.pointmerge(bm, verts=(pokev[0], sphv[2]), merge_co=pokev[0].co)

        # UVs
        islands = shared.bm_uv_cube_project(bm.faces, uv_layer)
        offset = Vec(0.5, islands['front'].bbox['b'] + 1.5)
        shared.bm_uv_cube_position(islands, uv_layer, init_offset=offset)
        cls.scale_uvs(bm.faces, uv_layer, islands)

        # mesh & object
        mesh = D.meshes.new('head')
        bm.to_mesh(mesh)
        bm.free()
        return D.objects.new(mesh.name, mesh)

    @classmethod
    def nose(cls) -> bpy.types.Object:
        # bmesh
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()
        conev = bmesh.ops.create_cone(bm, segments=3, radius1=1.0, radius2=0.0,
                                      depth=1.0)['verts']
        bmesh.ops.rotate(bm, verts=conev, matrix=Rotation(radians(90), 3, 'X'))
        bmesh.ops.scale(bm, verts=conev, vec=(0.02, 0.04, 0.04))
        bmesh.ops.translate(bm, verts=conev, vec=(0.0, -0.122, 1.443))
        conev[0].co.y -= 0.01

        # UVs
        bm.verts.ensure_lookup_table()
        for vert in bm.verts:
            for loop in vert.link_loops:
                loop[uv_layer].uv = bm.verts[3].co.xz
                loop[uv_layer].uv += Vec(0.5, 1.5)
        cls.scale_uvs(bm.faces, uv_layer)

        # mesh & object
        mesh = D.meshes.new('nose')
        bm.to_mesh(mesh)
        bm.free()
        return D.objects.new(mesh.name, mesh)

    @classmethod
    def neck(cls) -> bpy.types.Object:
        # bmesh
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()
        l1 = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=l1, vec=(0.07, 0.06, 1.0))
        bmesh.ops.scale(bm, verts=l1[2:], vec=(0.0, 1.07, 1.0))
        bmesh.ops.translate(bm, verts=l1, vec=(0.0, 0.02, 1.35))
        bmesh.ops.extrude_edge_only(bm, edges=bm.edges)
        bmesh.ops.translate(bm, verts=bm.verts[-4:], vec=(0.0, 0.0, 0.07))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

        # UVs
        bm.verts.ensure_lookup_table()
        for vert in bm.verts:
            for loop in vert.link_loops:
                loop[uv_layer].uv = bm.verts[5].co.xz
                loop[uv_layer].uv += Vec(0.5, 1.5)
        cls.scale_uvs(bm.faces, uv_layer)

        # mesh & object
        mesh = D.meshes.new('neck')
        bm.to_mesh(mesh)
        bm.free()
        return D.objects.new(mesh.name, mesh)

    @classmethod
    def torso(cls) -> bpy.types.Object:
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()

        luppertop = create_plane(bm, fill=True)['verts']
        bmesh.ops.scale(bm, verts=luppertop, vec=(0.14, 0.1, 1.0))
        bmesh.ops.translate(bm, verts=luppertop, vec=(0.0, 0.015, 1.352))

        luppermid = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=luppermid, vec=(0.24, 0.18, 1.0))
        bmesh.ops.translate(bm, verts=luppermid, vec=(0.0, -0.017, 1.21))

        lwaist = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=lwaist, vec=(0.14, 0.11, 1.0))
        bmesh.ops.translate(bm, verts=lwaist, vec=(0.0, -0.02, 1.076))

        lbot = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=lbot, vec=(0.23, 0.16, 1.0))
        bmesh.ops.translate(bm, verts=lbot, vec=(0.0, -0.004, 0.999))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                               dist=0.0000001, plane_co=(0, 0, 0),
                               plane_no=(1, 0, 0), clear_inner=True)

        islands = shared.bm_uv_cube_project(bm.faces, uv_layer)
        offset = Vec(0.5, islands['front'].bbox['b'] + 0.6)
        shared.bm_uv_cube_position(islands, uv_layer, init_offset=offset)
        cls.scale_uvs(bm.faces, uv_layer, islands)

        # mesh & object
        mesh = D.meshes.new('torso')
        bm.to_mesh(mesh)
        bm.free()
        object = D.objects.new(mesh.name, mesh)

        # texture & material
        texture = cls.torso_texture()
        material = cls.material(texture)
        object.data.materials.append(material)

        return object

    @classmethod
    def torso_texture(cls) -> bpy.types.Image:
        size = (512, 512)
        image = PIL.Image.new(mode='RGBA', size=size)
        draw = PIL.ImageDraw.Draw(image)

        # skirt
        draw.rectangle(xy=((256, 280), (317, 291)), fill=(48, 64, 112))
        draw.rectangle(xy=((256, 280), (317, 281)), fill=(24, 40, 88))

        # shirt
        draw.rectangle(xy=((256, 242), (317, 279)), fill=(224, 232, 232))
        draw.rectangle(xy=((265, 227), (262, 242)), fill=(224, 232, 232))
        draw.polygon(xy=((256, 242), (261, 242), (256, 250)), fill=(248, 208, 168))
        draw.line(xy=((256, 251), (260, 253), (265, 242), (317, 242)),
                  fill=(200, 200, 200))

        # mirror
        image.alpha_composite(image.transpose(PIL.Image.FLIP_LEFT_RIGHT))

        # buttons
        draw.line(xy=((256, 251), (256, 279)), fill=(200, 200, 200))
        for y in range(4):
            y *= 7
            draw.rectangle(xy=((253, 255 + y), (254, 256 + y)),
                           fill=(190, 190, 190))

        filepath = '03TmpTorso.png'
        image.save(filepath)
        return D.images.load(filepath, check_existing=True)

    @classmethod
    def arm(cls) -> bpy.types.Object:
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()

        l1 = create_plane(bm, fill=True)['verts']
        bmesh.ops.scale(bm, verts=l1, vec=(0.11, 0.07, 1.0))
        bmesh.ops.rotate(bm, verts=l1, cent=l1[0].co,
                         matrix=Rotation(radians(10), 4, 'Y'))
        bmesh.ops.translate(bm, verts=l1, vec=(0.12627, 0.019375, 1.3378))

        l4 = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=l4, vec=(0.06, 0.06, 1.0))
        bmesh.ops.rotate(bm, verts=l4, matrix=Rotation(radians(-10), 4, 'Y'))
        bmesh.ops.translate(bm, verts=l4, vec=(0.19385, 0.02, 1.0928))

        l5 = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=l5, vec=(0.08, 0.06, 1.0))
        bmesh.ops.rotate(bm, verts=l5, matrix=Rotation(radians(-12), 4, 'Y'))
        bmesh.ops.translate(bm, verts=l5, vec=(0.23261, 0.02, 0.94141))

        l6 = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=l6, vec=(0.12, 0.15, 1.0))
        bmesh.ops.translate(bm, verts=l6, vec=(0.24, 0.0, 0.81))
        bmesh.ops.translate(bm, verts=l6[1::1], vec=(0.0, 0.0, -0.01))
        bmesh.ops.translate(bm, verts=l6[2:3], vec=(0.03, 0.0, 0.0))

        l7 = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=l7, vec=(0.0, 0.12, 1.0))
        bmesh.ops.translate(bm, verts=l7, vec=(0.22202, 0.01375, 0.76588))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

        islands = shared.bm_uv_cube_project(bm.faces, uv_layer)
        offset = Vec(0.5, islands['front'].bbox['b'] + 1.25)
        shared.bm_uv_cube_position(islands, uv_layer, init_offset=offset)
        cls.scale_uvs(bm.faces, uv_layer, islands)

        mesh = D.meshes.new('arm')
        bm.to_mesh(mesh)
        bm.free()
        return D.objects.new(mesh.name, mesh)

    @classmethod
    def leg(cls) -> bpy.types.Object:
        # bmesh
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()

        ltop = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=ltop, vec=(0.16, 0.16, 1.0))
        bmesh.ops.scale(bm, verts=ltop[1::2], vec=(1.0, 1.15, 1.0))
        bmesh.ops.translate(bm, verts=ltop, vec=(0.08, 0.016, 0.83))
        bmesh.ops.translate(bm, verts=ltop[1::2], vec=(0.0, 0.0, 0.084))

        lmid = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=lmid, vec=(0.1, 0.1, 1.0))
        bmesh.ops.translate(bm, verts=lmid, vec=(0.065, 0.025, 0.55))

        lbot = create_plane(bm, fill=False)['verts']
        bmesh.ops.scale(bm, verts=lbot, vec=(0.1, 0.1, 1.0))
        bmesh.ops.translate(bm, verts=lbot, vec=(0.06566, 0.033125, 0.0))
        bmesh.ops.translate(bm, verts=lbot[0:2], vec=(0.0, 0.0, 0.15))

        lfeet = create_plane(bm, fill=True)['verts']
        bmesh.ops.scale(bm, verts=lfeet, vec=(0.1, 0.06, 1.0))
        bmesh.ops.translate(bm, verts=lfeet, vec=(0.06625, -0.178 + 0.03, 0.0))
        bmesh.ops.rotate(bm, verts=lfeet, cent=lfeet[0].co,
                         matrix=Rotation(radians(80), 4, 'X'))

        bmesh.ops.bridge_loops(bm, edges=bm.edges)

        # UVs
        islands = shared.bm_uv_cube_project(bm.faces, uv_layer)
        offset = Vec(0.5, islands['front'].bbox['b'])
        shared.bm_uv_cube_position(islands, uv_layer, init_offset=offset)
        cls.scale_uvs(bm.faces, uv_layer, islands)

        # mesh & object
        mesh = D.meshes.new('leg')
        bm.to_mesh(mesh)
        bm.free()
        object = D.objects.new(mesh.name, mesh)

        # texture & material
        texture = cls.leg_texture()
        material = cls.material(texture)
        object.data.materials.append(material)

        return object

    @classmethod
    def leg_texture(cls) -> bpy.types.Image:
        size = (512, 512)
        image = PIL.Image.new(mode='RGBA', size=size)
        draw = PIL.ImageDraw.Draw(image)

        # skirt
        draw.rectangle(xy=((256, 385), (390, 410)), fill=(48, 64, 112))
        draw.rectangle(xy=((256, 409), (390, 410)), fill=(24, 40, 88))

        # knee
        draw.ellipse(xy=((260, 437), (269, 448)), fill=(240, 176, 128))

        # shoe
        draw.rectangle(xy=((256, 489), (390, 512)), fill=(224, 232, 232))
        draw.rectangle(xy=((256, 378), (269, 384)), fill=(224, 232, 232))
        draw.rectangle(xy=((256, 325), (269, 361)), fill=(224, 232, 232))

        # mirror
        image.alpha_composite(image.transpose(PIL.Image.FLIP_LEFT_RIGHT))

        filepath = '03TmpLeg.png'
        image.save(filepath)
        return D.images.load(filepath, check_existing=True)

    @classmethod
    def pelvis(cls) -> bpy.types.Object:
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()

        # create pelvis from torso and leg
        bm_absorb_obj(bm, cls.torso())
        bm_absorb_obj(bm, cls.leg())
        bmesh.ops.bridge_loops(bm, edges=bm.edges[6:8] + bm.edges[17:18]
                               + bm.edges[25:29])
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[55:57], cuts=1)
        bm.verts.ensure_lookup_table()
        bm.verts[32].co = bm.verts[19].co
        bm.verts[33].co.y = bm.verts[19].co.y
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0001)

        # uvs
        islands = shared.bm_uv_cube_project(bm.faces[23:27], uv_layer)
        offset = Vec(0.5, islands['front'].bbox['b'] + 0.55)
        shared.bm_uv_cube_position(islands, uv_layer, init_offset=offset)
        cls.scale_uvs(bm.faces[23:27], uv_layer, islands)

        # mesh & object
        mesh = D.meshes.new('torso_pelvis_leg')
        bm.to_mesh(mesh)
        bm.free()
        object = D.objects.new(mesh.name, mesh)

        # texture & material
        texture = cls.pelvis_texture()
        material = cls.material(texture)
        object.data.materials.append(material)

        return object

    @classmethod
    def pelvis_texture(cls) -> bpy.types.Image:
        size = (512, 512)
        image = PIL.Image.new(mode='RGBA', size=size)
        draw = PIL.ImageDraw.Draw(image)
        draw.rectangle(xy=((256, 297), (330, 321)), fill=(48, 64, 112))
        image.alpha_composite(image.transpose(PIL.Image.FLIP_LEFT_RIGHT))

        filepath = '03TmpPelvis.png'
        image.save(filepath)
        return D.images.load(filepath, check_existing=True)

    @classmethod
    def material(cls, texture) -> bpy.types.Material:
        material = D.materials.new(name='material')
        material.use_nodes = True

        # nodes
        nodes = material.node_tree.nodes
        nodes.new('ShaderNodeTexImage')
        nodes['Image Texture'].image = texture
        nodes['Image Texture'].interpolation = 'Closest'
        nodes['Principled BSDF'].inputs['Specular'].default_value = 0.0

        # links
        links = material.node_tree.links
        links.new(nodes['Image Texture'].outputs['Color'],
                  nodes['Principled BSDF'].inputs['Base Color'])

        return material

    @classmethod
    def texture(cls) -> bpy.types.Image:
        img_out = PIL.Image.new(mode='RGBA', size=(512, 512), color=(248, 208, 168))
        for p in Path().glob('03Tmp*.png'):
            if str(p) in D.images:
                D.images.remove(D.images[str(p)])
            img_in = PIL.Image.open(p)
            img_out.alpha_composite(img_in)

        filepath = '03Texture.png'
        img_out.save(filepath)
        return D.images.load(filepath, check_existing=True)

if __name__ == '__main__':
    shared.delete_data()
    D.scenes[0].collection.objects.link(Character.object())
