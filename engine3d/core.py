import pygame, json

from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *

class PhysicsEngine:
    def __init__(self, gravity=Vector3(0, -9.8, 0)):
        self.gravity = gravity
        self.objects = []

    def update(self, dt):
        for obj in self.objects:
            if obj.physic:
                obj.apply_force(self.gravity)

            obj.update(dt)

        self.handle_collisions()

    def handle_collisions(self):
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1:]:
                if obj1.collision and obj2.collision:
                    if self.check_collision(obj1, obj2):
                        if obj1.physic:
                            self.resolve_collision(obj1, obj2)
                        elif obj2.physic:
                            self.resolve_collision(obj2, obj1)

    def resolve_collision(self, physics_obj, other_obj):
        relative_velocity = physics_obj.velocity - (other_obj.velocity if other_obj.physic else Vector3(0, 0, 0))
        collision_normal = (physics_obj.position - other_obj.position).normalize()

        if relative_velocity.dot(collision_normal) > 0:
            return

        e = min(physics_obj.restitution, other_obj.restitution)
        j = -(1 + e) * relative_velocity.dot(collision_normal)
        j /= physics_obj.inv_mass + (other_obj.inv_mass if other_obj.physic else 0)

        impulse = collision_normal * j

        physics_obj.velocity += impulse * physics_obj.inv_mass
        if other_obj.physic:
            other_obj.velocity -= impulse * other_obj.inv_mass

        penetration_depth = self.calculate_penetration_depth(physics_obj, other_obj)
        percent = 0.8
        slop = 0.01
        correction = max(penetration_depth - slop, 0) / (physics_obj.inv_mass + (other_obj.inv_mass if other_obj.physic else 0)) * percent * collision_normal

        physics_obj.position += correction * physics_obj.inv_mass
        if other_obj.physic:
            other_obj.position -= correction * other_obj.inv_mass

    @staticmethod
    def check_collision(obj1, obj2):
        min1, max1 = obj1.bounding_box
        min2, max2 = obj2.bounding_box
        return all(
            max1[i] + obj1.position[i] >= min2[i] + obj2.position[i] and
            min1[i] + obj1.position[i] <= max2[i] + obj2.position[i]
            for i in range(3)
        )

    @staticmethod
    def calculate_penetration_depth(obj1, obj2):
        min1, max1 = obj1.bounding_box
        min2, max2 = obj2.bounding_box
        overlap = [
            min(max1[i] + obj1.position[i], max2[i] + obj2.position[i]) -
            max(min1[i] + obj1.position[i], min2[i] + obj2.position[i])
            for i in range(3)
        ]
        return min(overlap)

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

        self.physics_engine = PhysicsEngine()

    def add_game_object(self, obj):
        self.game_objects.append(obj)
        self.physics_engine.objects.append(obj)

    def remove_game_object(self, obj):
        self.game_objects.remove(obj)
        self.physics_engine.objects.remove(obj)


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

        dt = self.clock.get_time() / 1000.0
        self.physics_engine.update(dt=dt)

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
