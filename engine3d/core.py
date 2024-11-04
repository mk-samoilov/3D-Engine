import pygame, json

from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *

from engine3d.camera import Camera


class Engine:
    def __init__(self, config: str = "config.json"):
        with open(file=f"{str(config)}", mode="r") as file:
            self.config = json.load(fp=file)

        self.last_mouse = (0, 0, 0)
        self.mouse_button_pressed = False

        pygame.init()
        self.width = self.config["window_width"]
        self.height = self.config["window_height"]
        self.display = pygame.display.set_mode(
            (
                self.width,
                self.height
            ), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.camera = Camera((0, 0, 5))
        self.game_objects = []

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.mouse_button_pressed = True
                    pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_button_pressed = False
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_button_pressed:
                    x_offset, y_offset = pygame.mouse.get_rel()
                    self.camera.rotate(x_offset, y_offset)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.camera.position += self.camera.front * 0.1
        if keys[pygame.K_s]:
            self.camera.position -= self.camera.front * 0.1
        if keys[pygame.K_a]:
            self.camera.position -= Vector3.cross(self.camera.front, self.camera.up).normalize() * 0.1
        if keys[pygame.K_d]:
            self.camera.position += Vector3.cross(self.camera.front, self.camera.up).normalize() * 0.1

        return True

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.camera.update()

        for game_object in self.game_objects:
            game_object.render()

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while self.handle_events():
            self.update()
        pygame.quit()
