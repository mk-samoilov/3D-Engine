import pygame, json

from engine3d.simple_objects import *

from OpenGL.GLU import *
from OpenGL.GL import *

class Engine:
    def __init__(self, window_size=(800, 600)):
        pygame.init()
        self.display = window_size
        pygame.display.set_mode(self.display, pygame.DOUBLEBUF | pygame.OPENGL)

        pygame.display.set_caption("Main Window")
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)

        glViewport(0, 0, self.display[0], self.display[1])
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)
        glEnable(GL_DEPTH_TEST)

        self.objects = []
        self.rotation_x, self.rotation_y = 0, 0

    def load_map(self, filename: str = "map.json"):
        with open(f"maps/{filename}", "r") as f:
            data = json.load(f)

        objects = []
        for obj_data in data["objects"]:
            if obj_data["type"] == "cube":
                cube = Cube(
                    vertices=obj_data["vertices"],
                    faces=obj_data["faces"],
                    colors=obj_data["colors"]
                )
                objects.append(cube)

        for obj in objects:
            self.add_object_on_map(obj)

    def add_object_on_map(self, obj):
        self.objects.append(obj)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotation_y -= 1
        if keys[pygame.K_RIGHT]:
            self.rotation_y += 1
        if keys[pygame.K_UP]:
            self.rotation_x -= 1
        if keys[pygame.K_DOWN]:
            self.rotation_x += 1

        return True

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        for obj in self.objects:
            obj.draw()

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            self.update()
            clock.tick(60)

        pygame.quit()
