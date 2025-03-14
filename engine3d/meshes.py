import math

from .classes import Mesh

def gen_cube(width: float, height: float, depth: float) -> Mesh:
    w = float(width) * 2
    h = float(height) * 2
    d = float(depth) * 2

    vertices = [
        [-w/2, -h/2, -d/2], [w/2, -h/2, -d/2], [w/2, h/2, -d/2], [-w/2, h/2, -d/2],
        [-w/2, -h/2, d/2], [w/2, -h/2, d/2], [w/2, h/2, d/2], [-w/2, h/2, d/2]
    ]

    faces = [
        [0, 1, 2], [0, 2, 3],
        [5, 4, 7], [5, 7, 6],
        [4, 5, 1], [4, 1, 0],
        [3, 2, 6], [3, 6, 7],
        [7, 4, 0], [7, 0, 3],
        [1, 5, 6], [1, 6, 2]
    ]

    uvs = [
        [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 1], [0, 1]],
        [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 1], [0, 1]],
        [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 1], [0, 1]],
        [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 1], [0, 1]],
        [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 1], [0, 1]],
        [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 1], [0, 1]]
    ]

    return Mesh(vertices=vertices, faces=faces, uvs=uvs)

def gen_sphere(radius: float, segments: int = 16) -> Mesh:
    vertices = []
    faces = []
    uvs = []

    for i in range(segments + 1):
        theta = i * math.pi / segments
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)

        for j in range(segments + 1):
            phi = j * 2 * math.pi / segments
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)

            x = radius * sin_theta * cos_phi
            y = radius * cos_theta
            z = radius * sin_theta * sin_phi

            vertices.append([x, y, z])

    for i in range(segments):
        for j in range(segments):
            v0 = i * (segments + 1) + j
            v1 = v0 + 1
            v2 = (i + 1) * (segments + 1) + j + 1
            v3 = v2 - 1

            faces.append([v0, v1, v2])
            faces.append([v0, v2, v3])

            u0 = j / segments
            u1 = (j + 1) / segments
            v0 = i / segments
            v1 = (i + 1) / segments

            uvs.append([[u0, v0], [u1, v0], [u1, v1]])
            uvs.append([[u0, v0], [u1, v1], [u0, v1]])

    return Mesh(vertices=vertices, faces=faces, uvs=uvs)
