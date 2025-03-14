from pygame.math import Vector3

from OpenGL.GL import *

class Light:
    def __init__(self, position: tuple, color: tuple = (1.0, 1.0, 1.0), ambient: float = 0.2, diffuse: float = 0.8, specular: float = 1.0):
        self.position = Vector3(position)
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.light_id = None

    def setup(self, light_id: int):
        self.light_id = light_id
        glEnable(GL_LIGHTING)
        glEnable(light_id)

        glLightfv(light_id, GL_AMBIENT, [self.color[0] * self.ambient,
                                         self.color[1] * self.ambient,
                                         self.color[2] * self.ambient, 1.0])
        glLightfv(light_id, GL_DIFFUSE, [self.color[0] * self.diffuse,
                                         self.color[1] * self.diffuse,
                                         self.color[2] * self.diffuse, 1.0])
        glLightfv(light_id, GL_SPECULAR, [self.color[0] * self.specular,
                                          self.color[1] * self.specular,
                                          self.color[2] * self.specular, 1.0])

        glLightf(light_id, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(light_id, GL_LINEAR_ATTENUATION, 0.1)
        glLightf(light_id, GL_QUADRATIC_ATTENUATION, 0.01)

    def update(self):
        if self.light_id is not None:
            glLightfv(self.light_id, GL_POSITION, [*self.position, 1.0])
