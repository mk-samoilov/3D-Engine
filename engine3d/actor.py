import numpy as np

from pygame.math import Vector3
from OpenGL.GL import *

class Actor:
    def __init__(self, position, mesh):
        self.position = Vector3(position)
        self.vertices = np.array(mesh.vertices, dtype=np.float32)
        self.faces = np.array(mesh.faces, dtype=np.int32)

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_id in face:
                glVertex3fv(self.vertices[vertex_id])
        glEnd()
        glPopMatrix()
