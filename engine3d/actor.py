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
        self.bounding_box = self.calculate_bounding_box()
        self.collision = mesh.collision

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

    def calculate_bounding_box(self):
        min_cords = np.min(self.vertices, axis=0)
        max_cords = np.max(self.vertices, axis=0)
        return min_cords, max_cords

    def check_collision(self, point):
        min_cords, max_cords = self.bounding_box
        return all(min_cords[i] + self.position[i] <= point[i] <= max_cords[i] + self.position[i] for i in range(3))