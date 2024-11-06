class Mesh:
    def __init__(self, vertices: list, faces: list, uvs: list, collision: bool):
        self.vertices = vertices
        self.faces = faces
        self.uvs = uvs
        self.collision = collision
