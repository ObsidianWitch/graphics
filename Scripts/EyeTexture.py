#!/usr/bin/env python3

import PIL.Image, PIL.ImageDraw # https://pypi.org/project/Pillow/

def ellipse_helper(draw, size, scale=(1.0, 1.0), translate=(0, 0), **kwargs):
    x1 = size[0] * scale[0]
    y1 = size[1] * scale[1]
    x0 = translate[0] + abs(size[0] - x1)
    y0 = translate[1] + abs(size[1] - y1)
    x1 += translate[0]
    y1 += translate[1]
    draw.ellipse(xy=(x0, y0, x1, y1), **kwargs)

def eye_texture(size):
    image = PIL.Image.new('RGBA', size)
    draw0 = PIL.ImageDraw.Draw(image)

    # iris & pupil
    ellipse_helper(draw0, size, scale=(0.99, 0.99), fill=(150, 14, 0))
    ellipse_helper(draw0, size, scale=(0.9, 0.94), fill=(255, 192, 43))

    ellipse_helper(draw0, size, scale=(0.7, 0.8), outline=(248, 169, 0), width=2)
    ellipse_helper(draw0, size, scale=(0.52, 0.94), fill=(248, 169, 0))
    ellipse_helper(draw0, size, scale=(0.9, 0.52), fill=(248, 169, 0))

    ellipse_helper(draw0, size, scale=(0.56, 0.66), fill=(143, 9, 0))

    # shadow
    shadow = PIL.Image.new('RGBA', size)
    draw1 = PIL.ImageDraw.Draw(shadow)
    ellipse_helper(draw1, size, scale=(0.99, 0.99), fill=(0, 0, 0, 40))
    ellipse_helper(draw1, size, scale=(0.99, 0.99), translate=(0, size[1] // 3),
                   fill=(0, 255, 0))
    shadow.putdata(tuple(
        (0, 0, 0, 0) if color == (0, 255, 0, 255) else color
        for color in shadow.getdata()
    ))
    image.alpha_composite(shadow)

    # specular highlights
    draw0.ellipse(
        xy=((size[0] * 0.62, size[1] * 0.3), (size[0] * 0.72, size[1] * 0.38)),
        fill=(255, 255, 255),
    )
    draw0.ellipse(
        xy=((size[0] * 0.7, size[1] * 0.4), (size[0] * 0.74, size[1] * 0.43)),
        fill=(255, 255, 255),
    )

    image.save(f'out/EyeTexture_{size[0]}x{size[1]}.png')

if __name__ == "__main__":
    eye_texture(size=(54, 78))
