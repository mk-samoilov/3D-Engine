from OpenGL.GL import *

class Cube:
    def __init__(self, vertices, faces, colors):
        self.vertices = vertices
        self.faces = faces
        self.colors = colors
        self.edges = self.generate_edges()

    def generate_edges(self):
        edges = set()
        for face in self.faces:
            for i in range(len(face)):
                edge = tuple(sorted([face[i], face[(i + 1) % len(face)]]))
                edges.add(edge)
        return list(edges)

    def draw(self):
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            glColor3fv(self.colors[i])
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glColor3fv((1, 1, 1))
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()
