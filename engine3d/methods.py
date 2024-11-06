import json

from PIL import Image
from OpenGL.GL import *

from engine3d.mesh import Mesh

def load_mesh_on_file(file: str):
    with open(file=f"{str(file)}", mode="r") as file:
        mesh_data = json.load(fp=file)
        mesh = Mesh(
            vertices=mesh_data["vertices"],
            faces=mesh_data["faces"],
            uvs=mesh_data["uvs"],
            collision=mesh_data["collision"]
        )

    return mesh


def load_texture_on_file(file: str):
    image = Image.open(file)
    image_data = image.convert("RGBA").tobytes()
    width, height = image.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id
