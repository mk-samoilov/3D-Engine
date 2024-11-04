from pygame.math import Vector3
from OpenGL.GLU import *
import math

class Camera:
    def __init__(self, position):
        self.position = Vector3(position)
        self.front = Vector3(0, 0, -1)
        self.up = Vector3(0, 1, 0)
        self.yaw = -90
        self.pitch = 0

    def update(self):
        gluLookAt(
            self.position.x, self.position.y, self.position.z,
            self.position.x + self.front.x,
            self.position.y + self.front.y,
            self.position.z + self.front.z,
            self.up.x, self.up.y, self.up.z
        )

    def rotate(self, x_offset, y_offset):
        sensitivity = 0.1
        self.yaw += x_offset * sensitivity
        self.pitch -= y_offset * sensitivity

        self.pitch = max(-89, min(89, self.pitch))

        front = Vector3()
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.front = front.normalize()
