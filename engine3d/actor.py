import numpy as np
from pygame.math import Vector3
from OpenGL.GL import *

class Actor:
    def __init__(self, position, rotation, mesh, texture, collision: bool, physic: bool = False, mass: float = 1.0, restitution: float = 0.5):
        self.position = Vector3(position)
        self.rotation = Vector3(rotation)
        self.velocity = Vector3(0, 0, 0)
        self.angular_velocity = Vector3(0, 0, 0)
        self.vector = Vector3(0, 0, 0)

        self.physic = physic
        self.mass = mass
        self.inv_mass = 1 / mass if mass != 0 else 0
        self.restitution = restitution

        self.vertices = np.array(mesh.vertices, dtype=np.float32)
        self.faces = np.array(mesh.faces, dtype=np.int32)
        self.uvs = np.array(mesh.uvs, dtype=np.float32)
        self.texture = texture
        self.bounding_box = self.calculate_bounding_box()
        self.collision = collision

        self.inertia_tensor = self.calculate_inertia_tensor()
        self.inv_inertia_tensor = np.linalg.inv(self.inertia_tensor)
        self.friction = 0.3
        self.applied_force = Vector3(0, 0, 0)

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

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

    def calculate_inertia_tensor(self):
        inertia = np.zeros((3, 3))
        for vertex in self.vertices:
            x_, y, z = vertex
            inertia[0, 0] += y**2 + z**2
            inertia[1, 1] += x_**2 + z**2
            inertia[2, 2] += x_**2 + y**2
            inertia[0, 1] -= x_ * y
            inertia[0, 2] -= x_ * z
            inertia[1, 2] -= y * z
        inertia[1, 0] = inertia[0, 1]
        inertia[2, 0] = inertia[0, 2]
        inertia[2, 1] = inertia[1, 2]
        return inertia * self.mass

    def check_collision(self, point):
        min_cords, max_cords = self.bounding_box
        return all(min_cords[i] + self.position[i] <= point[i] <= max_cords[i] + self.position[i] for i in range(3))

    def apply_force(self, force: Vector3):
        self.applied_force += force

    def apply_impulse(self, impulse: Vector3, point: Vector3 = None):
        self.velocity += impulse * self.inv_mass
        if point:
            torque = Vector3.cross(point - self.position, impulse)
            self.apply_torque(torque)

    def apply_torque(self, torque: Vector3):
        self.angular_velocity += Vector3(*np.dot(self.inv_inertia_tensor, torque))

    def update(self, dt: float):
        # F = ma, a = F/m

        dt = float(dt)
        self.vector = self.applied_force

        self.velocity += self.vector / self.mass * dt
        self.position += self.velocity * dt

        angle = self.angular_velocity.magnitude() * dt
        if angle != 0:
            axis = self.angular_velocity.normalize()
            self.rotate(angle, axis)

        self.applied_force = Vector3(0, 0, 0)

    def rotate(self, angle: float, axis: Vector3):
        quat = [axis.x * np.sin(angle/2), axis.y * np.sin(angle/2), axis.z * np.sin(angle/2), np.cos(angle/2)]
        self.rotation = Vector3(*self.quaternion_multiply(quat, [*self.rotation, 0])[:3])

    @staticmethod
    def quaternion_multiply(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return [
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        ]
