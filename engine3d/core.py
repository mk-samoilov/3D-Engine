from pygame.math import Vector3

from OpenGL.GL import *
from OpenGL.GLU import *

import threading
import time
import importlib
import curses
import os
import pygame

from .actor import Actor
from .hud import HUDComponent
from .light import Light

class PhysicsEngine:
    def __init__(self, gravity: Vector3 = Vector3(0, 0, 0)): # Vector3(0, -9.8, 0) - earth gravity
        self.gravity = gravity
        self.objects = []

    def update(self, dt: float):
        for obj in self.objects:
            if obj.physic:
                gravitational_force = self.gravity
                obj.apply_force(gravitational_force)
            obj.update(dt=float(dt))

        self.handle_collisions()

    def handle_collisions(self):
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1:]:
                if obj1.collision and obj2.collision:
                    if self.check_collision(obj1, obj2):
                        self.resolve_collision(obj1, obj2)

    def resolve_collision(self, obj1, obj2):
        if not (obj1.physic or obj2.physic):
            return

        collision_point = self.find_collision_point(obj1, obj2)
        collision_normal = (obj2.position - obj1.position).normalize()

        rel_velocity = obj2.velocity - obj1.velocity
        if obj1.physic and obj2.physic:
            rel_velocity += Vector3.cross(obj2.angular_velocity, collision_point - obj2.position)
            rel_velocity -= Vector3.cross(obj1.angular_velocity, collision_point - obj1.position)

        rel_normal_velocity = rel_velocity.dot(collision_normal)
        if rel_normal_velocity > 0:
            return

        e = min(obj1.restitution, obj2.restitution)
        j = -(1 + e) * rel_normal_velocity
        j /= obj1.inv_mass + obj2.inv_mass

        impulse = collision_normal * j

        if obj1.physic:
            obj1.apply_impulse(-impulse, collision_point - obj1.position)
        if obj2.physic:
            obj2.apply_impulse(impulse, collision_point - obj2.position)

        tangent = rel_velocity - (rel_velocity.dot(collision_normal) * collision_normal)
        if tangent.magnitude() > 0:
            tangent = tangent.normalize()
            friction_impulse = -tangent * j * min(obj1.friction, obj2.friction)

            if obj1.physic:
                obj1.apply_impulse(-friction_impulse, collision_point - obj1.position)
            if obj2.physic:
                obj2.apply_impulse(friction_impulse, collision_point - obj2.position)

        penetration_depth = self.calculate_penetration_depth(obj1, obj2)
        percent = 0.8
        slop = 0.01
        correction = max(penetration_depth - slop, 0) / (obj1.inv_mass + obj2.inv_mass) * percent * collision_normal

        if obj1.physic:
            obj1.position -= correction * obj1.inv_mass
        if obj2.physic:
            obj2.position += correction * obj2.inv_mass

    @staticmethod
    def find_collision_point(obj1, obj2):
        # Simplified collision point calculation (center of overlap)
        return (obj1.position + obj2.position) * 0.5

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
    def __init__(self, player, config: str = "config", console_inside_game: bool = True):
        self.console_ = self.ConsoleComponent(core_class_instance=self)
        curses.wrapper(self.console_.__run__)

        self.console_.print("Initialization Engine3D...")

        self.config = importlib.import_module(name=str(config))

        self.last_mouse = (0, 0, 0)
        self.unlocked_rotation_camera = False

        pygame.init()
        pygame.font.init()

        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, self.config.MSAA_X)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, self.config.MSAA_X)
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, self.config.MSAA_X)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

        self.handling = True

        self.display = pygame.display.set_mode(
            (
                self.config.WINDOW_WIDTH,
                self.config.WINDOW_HEIGHT
            ), pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.display.set_icon(pygame.image.load(self.config.WINDOW_ICON))

        self.custom_update_functions = []

        self.clock = pygame.time.Clock()
        self.player = player
        self.game_objects = []
        self.lights = []
        self.max_lights = 8

        pygame.display.set_caption(self.config.WINDOW_TITLE)

        self.console_inside_game = bool(console_inside_game)
        self.game_console_history = []

        self.fonts = self.Fonts(core_class_instance=self, fonts_folder="./engine3d/fonts")

        self.console_.print("Initialization OpenGL...")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glViewport(0, 0, self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.config.WINDOW_WIDTH / self.config.WINDOW_HEIGHT), 0.1, self.config.DRAW_DISTANCE)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT7)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        self.render_loading_screen()

        self.console_.print("Initialization HUD component...")

        self.hud_component = HUDComponent()

        self.console_.print("Initialization PhysicsEngine component...")

        self.physics_engine = PhysicsEngine()
        self.fixed_time_step = 1 / 60
        self.accumulated_time = 0

        self.loading_complete = False

        self.console_.print("Done loading core components.")

    class ConsoleComponent:
        def __init__(self, core_class_instance) -> None:
            self.down_bar: str = "ENGINE3D LOGS"
            self.lines: list = []

            self.core = core_class_instance

            self.top_line = 0
            self.left_margin = 0

            self.handling = True

            self.COLOR_PAIRS = \
                [
                    {"pair-code": 1, "text": curses.COLOR_BLUE, "background": curses.COLOR_BLACK},
                    {"pair-code": 2, "text": curses.COLOR_GREEN, "background": curses.COLOR_BLACK},
                    {"pair-code": 3, "text": curses.COLOR_YELLOW, "background": curses.COLOR_BLACK},
                    {"pair-code": 4, "text": curses.COLOR_CYAN, "background": curses.COLOR_BLACK}
                ]

        def __run__(self, stdscr) -> None:
            self.stdscr = stdscr
            self.stdscr.clear()

            curses.curs_set(0)

            curses.start_color()
            for pair in self.COLOR_PAIRS:
                curses.init_pair(pair["pair-code"], pair["text"], pair["background"])

            threading.Thread(target=self.loop).start()

        def loop(self) -> None:
            try:
                while self.handling:
                    self.display()
                    time.sleep(0.1)
            except KeyboardInterrupt: pass
            finally:
                self.handling = False
                self.core.handling = False

        def print(self, string: str) -> None:
            self.lines.append(str(string))
            height, _ = self.stdscr.getmaxyx()
            visible_height = height - 1
            if self.top_line + visible_height >= len(self.lines) - 1:
                self.top_line = max(0, len(self.lines) - visible_height)

        def display(self) -> None:
            height, width = self.stdscr.getmaxyx()
            self.stdscr.clear()

            for y, line in enumerate(self.lines[self.top_line:self.top_line + height - 1]):
                if y == height - 1:
                    break

                visible_line = line[self.left_margin:self.left_margin + width]
                self.stdscr.addstr(y, 0, visible_line)

            self.stdscr.addstr(height - 1, 0, self.down_bar, curses.A_REVERSE)

            self.stdscr.refresh()

    class Fonts:
        def __init__(self, core_class_instance, fonts_folder: str ="fonts"):
            pygame.font.init()
            self.core = core_class_instance
            self._load_fonts(str(fonts_folder))

        def _load_fonts(self, folder_path):
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created fonts folder: {folder_path}")
                return

            font_extensions = (".ttf", ".otf")

            for filename in os.listdir(folder_path):
                if filename.lower().endswith(font_extensions):
                    font_name = os.path.splitext(filename)[0]
                    font_path = os.path.join(folder_path, filename)
                    try:
                        setattr(self, font_name, pygame.font.Font(font_path, int(self.core.config.WINDOW_WIDTH / 100)))
                        self.core.console_.print(f"Loaded font: {font_name}")
                    except Exception as e:
                        self.core.console_.print(f"ERROR loading font: '{e}', loading default system font...")
                        setattr(self, font_name, pygame.font.SysFont(None, int(self.core.config.WINDOW_WIDTH / 100)))

    def render_inside_console(self):
        pass

    def add_game_object(self, obj: Actor):
        self.game_objects.append(obj)
        self.physics_engine.objects.append(obj)

    def remove_game_object(self, obj: Actor):
        self.game_objects.remove(obj)
        self.physics_engine.objects.remove(obj)

    def add_light(self, light: Light):
        if len(self.lights) < self.max_lights:
            light.setup(GL_LIGHT0 + len(self.lights))
            self.lights.append(light)
            return True
        return False

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

    def render_loading_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.config.WINDOW_WIDTH, 0, self.config.WINDOW_HEIGHT, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

        font = self.fonts.default_2
        text_surface = font.render("Loading scene and assets...", True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        text_x = (self.config.WINDOW_WIDTH - text_surface.get_width()) // 2
        text_y = (self.config.WINDOW_HEIGHT - text_surface.get_height()) // 2

        glRasterPos2f(text_x, text_y)
        glDrawPixels(
            text_surface.get_width(),
            text_surface.get_height(),
            GL_RGBA, GL_UNSIGNED_BYTE, text_data
        )

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        pygame.display.flip()

    def load_all_objects(self):
        for obj in self.game_objects:
            obj.__setup_vbo__()
            self.console_.print(f"Loaded object at {obj.position}")

        self.loading_complete = True
        self.console_.print("Scene and assets loaded.")

    def add_update_function(self, func):
        self.custom_update_functions.append(func)

    def remove_update_function(self, func):
        self.custom_update_functions.remove(func)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.player.update()

        dt = self.clock.get_time() / 1000.0
        self.accumulated_time += dt

        while self.accumulated_time >= self.fixed_time_step:
            self.physics_engine.update(dt=self.fixed_time_step)
            self.accumulated_time -= self.fixed_time_step

        for light in self.lights:
            light.update()

        for game_object in self.game_objects:
            game_object.render()

        for func in self.custom_update_functions:
            func()

        self.hud_component.render_all_hud(
            window_width=self.config.WINDOW_WIDTH,
            window_height=self.config.WINDOW_HEIGHT
        )

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        try:
            while not self.loading_complete:
                self.load_all_objects()
                pygame.event.pump()

            while self.handling and self.handle_events():
                self.update()
        except KeyboardInterrupt:
            pass
        finally:
            self.handling = False
            self.console_.handling = False
            pygame.quit()
