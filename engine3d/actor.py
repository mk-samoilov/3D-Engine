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
        self.normals = self.calculate_normals()

        self.inertia_tensor = self.calculate_inertia_tensor()
        self.inv_inertia_tensor = np.linalg.inv(self.inertia_tensor)
        self.friction = 0.3
        self.applied_force = Vector3(0, 0, 0)

        self.__setup_vbo__()

    def __setup_vbo__(self):
        self.vbo = glGenBuffers(1)
        self.ibo = glGenBuffers(1)
        self.nbo = glGenBuffers(1)
        self.tbo = glGenBuffers(1)

        vertex_data = []
        normal_data = []
        uv_data = []
        index_data = []

        for face_idx, (face, uv_face) in enumerate(zip(self.faces, self.uvs)):
            for vertex_id, uv in zip(face, uv_face):
                vertex_data.extend(self.vertices[vertex_id])
                normal_data.extend(self.normals[vertex_id])
                uv_data.extend(uv)
                index_data.append(face_idx * 3 + list(face).index(vertex_id))

        vertex_data = np.array(vertex_data, dtype=np.float32)
        normal_data = np.array(normal_data, dtype=np.float32)
        uv_data = np.array(uv_data, dtype=np.float32)
        index_data = np.array(index_data, dtype=np.uint32)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, self.nbo)
        glBufferData(GL_ARRAY_BUFFER, normal_data.nbytes, normal_data, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, self.tbo)
        glBufferData(GL_ARRAY_BUFFER, uv_data.nbytes, uv_data, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

        self.num_indices = len(index_data)

    def calculate_normals(self):
        normals = np.zeros_like(self.vertices)
        for face in self.faces:
            v0, v1, v2 = [self.vertices[i] for i in face]
            normal = np.cross(v1 - v0, v2 - v0)
            normal = normal / (np.linalg.norm(normal) or 1)
            for vertex_id in face:
                normals[vertex_id] += normal
        return normals / (np.linalg.norm(normals, axis=1)[:, np.newaxis] + 1e-6)

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation.x, 1, 0, 0)
        glRotatef(self.rotation.y, 0, 1, 0)
        glRotatef(self.rotation.z, 0, 0, 1)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_TEXTURE_2D)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.nbo)
        glNormalPointer(GL_FLOAT, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.tbo)
        glTexCoordPointer(2, GL_FLOAT, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glDrawElements(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, None)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

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
