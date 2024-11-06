import math
import json

def generate_cylinder(radius=1.0, height=2.0, segments=32, collision=False):
    vertices = []
    faces = []
    uvs = []

    vertices.append([0, height / 2, 0])
    vertices.append([0, -height / 2, 0])

    for i in range(segments):
        angle = (2.0 * math.pi * i) / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)

        vertices.append([x, height / 2, z])
        vertices.append([x, -height / 2, z])

    for i in range(segments):
        current = 2 + i * 2
        _next = 2 + ((i + 1) % segments) * 2

        faces.append([0, current, _next])

        u1 = 0.5 + math.cos(angle) * 0.5
        v1 = 0.5 + math.sin(angle) * 0.5
        uvs.append([[0.5, 0.5], [u1, v1],
                    [0.5 + math.cos((2.0 * math.pi * (i + 1)) / segments) * 0.5,
                     0.5 + math.sin((2.0 * math.pi * (i + 1)) / segments) * 0.5]])

        # Bottom face
        faces.append([1, current + 1, _next + 1])
        uvs.append([[0.5, 0.5], [u1, v1],
                    [0.5 + math.cos((2.0 * math.pi * (i + 1)) / segments) * 0.5,
                     0.5 + math.sin((2.0 * math.pi * (i + 1)) / segments) * 0.5]])

        faces.append([current, current + 1, _next + 1])
        faces.append([current, _next + 1, _next])

        u_current = i / segments
        u_next = (i + 1) / segments
        uvs.append([[u_current, 1], [u_current, 0], [u_next, 0]])
        uvs.append([[u_current, 1], [u_next, 0], [u_next, 1]])

    cylinder_data = {
        "collision": collision,
        "vertices": vertices,
        "faces": faces,
        "uvs": uvs
    }

    with open("cylinder.json", "w") as f:
        json.dump(cylinder_data, f, indent=2)

    return cylinder_data

cylinder = generate_cylinder(radius=1.1, height=2.5, segments=64, collision=True)
