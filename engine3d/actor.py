import numpy

from pygame.math import Vector3
from OpenGL.GL import *

class Actor:
    def __init__(self, position, rotation, mesh, texture, collision: bool, physic: bool = False, mass: float = 1.0, restitution: float = 0.5):
        self.position = Vector3(position)
        self.rotation = Vector3(rotation)
        self.velocity = Vector3(0, 0, 0)
        self.angular_velocity = Vector3(0, 0, 0)
        self.acceleration = Vector3(0, 0, 0)

        self.physic = physic
        self.mass = mass
        self.inv_mass = 1 / mass if mass != 0 else 0
        self.restitution = restitution

        self.vertices = numpy.array(mesh.vertices, dtype=numpy.float32)
        self.faces = numpy.array(mesh.faces, dtype=numpy.int32)
        self.uvs = numpy.array(mesh.uvs, dtype=numpy.float32)
        self.texture = texture
        self.bounding_box = self.calculate_bounding_box()
        self.collision = collision

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[0], 0, 0, 1)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 1, 0, 0)

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
        min_cords = numpy.min(self.vertices, axis=0)
        max_cords = numpy.max(self.vertices, axis=0)
        return min_cords, max_cords

    def check_collision(self, point):
        min_cords, max_cords = self.bounding_box
        return all(min_cords[i] + self.position[i] <= point[i] <= max_cords[i] + self.position[i] for i in range(3))

    def apply_force(self, force):
        self.acceleration += force * self.inv_mass

    def apply_torque(self, torque):
        self.angular_velocity += torque * self.inv_mass

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        self.rotation += Vector3(
            self.angular_velocity.x * dt * 57.2958,
            self.angular_velocity.y * dt * 57.2958,
            self.angular_velocity.z * dt * 57.2958
        )

        self.rotation.x = self.rotation.x % 360
        self.rotation.y = self.rotation.y % 360
        self.rotation.z = self.rotation.z % 360

        self.acceleration = Vector3(0, 0, 0)
