import numpy as np
from pygame.math import Vector3
from OpenGL.GL import *


class Actor:
    def __init__(self, position, mesh, texture):
        self.position = Vector3(position)
        self.vertices = np.array(mesh.vertices, dtype=np.float32)
        self.faces = np.array(mesh.faces, dtype=np.int32)
        self.uvs = np.array(mesh.uvs, dtype=np.float32)
        self.texture = texture

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_TEXTURE_2D)

        glBegin(GL_TRIANGLES)
        for face, uv_face in zip(self.faces, self.uvs):
            for vertex_id, uv in zip(face, uv_face):
                glTexCoord2fv(uv)
                glVertex3fv(self.vertices[vertex_id])
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
