from pygame.math import Vector3
from OpenGL.GLU import *

class Camera:
    def __init__(self, position):
        self.position = Vector3(position)
        self.front = Vector3(0, 0, -1)
        self.up = Vector3(0, 1, 0)

    def update(self):
        gluLookAt(
            self.position.x, self.position.y, self.position.z,
            self.position.x + self.front.x,
            self.position.y + self.front.y,
            self.position.z + self.front.z,
            self.up.x, self.up.y, self.up.z
        )