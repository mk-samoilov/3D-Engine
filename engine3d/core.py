import pygame, json

from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *

class Engine:
    def __init__(self, player, config: str = "config.json"):
        with open(file=f"{str(config)}", mode="r") as file:
            self.config = json.load(fp=file)

        self.last_mouse = (0, 0, 0)
        self.unlocked_rotation_camera = False

        pygame.init()
        self.width = self.config["window_width"]
        self.height = self.config["window_height"]
        self.display = pygame.display.set_mode(
            (
                self.width,
                self.height
            ), pygame.OPENGL | pygame.DOUBLEBUF)

        self.window_icon = pygame.image.load(self.config["window_icon"])
        pygame.display.set_icon(self.window_icon)

        self.custom_update_functions = []

        self.clock = pygame.time.Clock()
        self.player = player
        self.game_objects = []

        pygame.display.set_caption(self.config["window_name"])

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
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
                    self.unlocked_rotation_camera = True
                    pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.unlocked_rotation_camera = False
            elif event.type == pygame.MOUSEMOTION:
                if self.unlocked_rotation_camera:
                    x_offset, y_offset = pygame.mouse.get_rel()
                    self.player.rotate(x_offset, y_offset)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.player.move(self.player.front * 0.1, self.game_objects)
        if keys[pygame.K_s]:
            self.player.move(-self.player.front * 0.1, self.game_objects)
        if keys[pygame.K_a]:
            self.player.move(-Vector3.cross(self.player.front, self.player.up).normalize() * 0.1, self.game_objects)
        if keys[pygame.K_d]:
            self.player.move(Vector3.cross(self.player.front, self.player.up).normalize() * 0.1, self.game_objects)

        return True

    def add_update_function(self, func):
        self.custom_update_functions.append(func)

    def remove_update_function(self, func):
        self.custom_update_functions.remove(func)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.player.update()

        for game_object in self.game_objects:
            game_object.render()

        for func in self.custom_update_functions:
            func()

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while self.handle_events():
            self.update()
        pygame.quit()
