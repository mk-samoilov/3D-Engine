import math

from typing import List, Tuple
from pygame.math import Vector3
from OpenGL.GLU import *

from engine3d.actor import Actor

class Camera:
    def __init__(self, position: Tuple, collision: bool):
        self.position = Vector3(position)
        self.front = Vector3(0, 0, -1)
        self.up = Vector3(0, 1, 0)
        self.yaw = -90
        self.pitch = 0
        self.collision = collision

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

    def move(self, direction, game_objects: List[Actor]):
        new_position = self.position + direction
        for obj in game_objects:
            if obj.check_collision(new_position) and obj.collision and self.collision:
                closest_point = self.find_closest_point(new_position, obj)
                try:
                    self.position = closest_point + (new_position - closest_point).normalize()
                except ValueError:
                    pass
                finally:
                    return
        self.position = new_position

    @staticmethod
    def find_closest_point(point, obj):
        min_cords, max_cords = obj.bounding_box
        closest = Vector3()
        for i in range(3):
            closest[i] = max(min_cords[i] + obj.position[i], min(point[i], max_cords[i] + obj.position[i]))
        return closest
