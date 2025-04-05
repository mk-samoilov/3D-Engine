from pygame.math import Vector3

from OpenGL.GL import *
from OpenGL.GLU import *

import importlib

import sys
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

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

class Engine3D:
    def __init__(self, player, config: str = "config"):
        self.config = importlib.import_module(name=str(config))

        if not glfw.init():
            sys.exit(1)

        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)
        width = mode.size.width
        height = mode.size.height

        self.window = self.init_window(width=width, height=height, title=self.config.WINDOW_TITLE, monitor=monitor)
        glfw.make_context_current(self.window)

        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

        self.frame_time = 1.0 / self.config.TARGET_FPS
        self._frame_start_time = None

        self.running = True

        self.custom_update_functions = []
        self.game_objects = []
        self.lights = []
        self.max_lights = 8
        self.physics_engine = PhysicsEngine()
        self.fixed_time_step = 1 / 60
        self.accumulated_time = 0
        self.hud_component = HUDComponent()

        self.player = player

        self.last_time = glfw.get_time()
        self.last_mouse_x = width / 2
        self.last_mouse_y = height / 2
        self.mouse_locked = False
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, bytes([0, 255, 255]))

    def init_window(self, width: int, height: int, title: str, monitor):
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
        glfw.window_hint(glfw.SAMPLES, self.config.MSAA_X)

        glfw.window_hint(glfw.MAXIMIZED, glfw.TRUE)

        window = glfw.create_window(width, height, title, monitor, None)
        if not window:
            glfw.terminate()
            sys.exit(1)
        return window

    def handle_inputs(self):
        if glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS and not self.mouse_locked:
            self.mouse_locked = True
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            glfw.set_cursor_pos(self.window, self.last_mouse_x, self.last_mouse_y)
        elif glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT) == glfw.RELEASE and self.mouse_locked:
            self.mouse_locked = False
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

        if self.mouse_locked:
            x_, y = glfw.get_cursor_pos(self.window)
            x_offset = x_ - self.last_mouse_x
            y_offset = y - self.last_mouse_y
            self.last_mouse_x = x_
            self.last_mouse_y = y
            self.player.rotate(x_offset, y_offset)

        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.player.move(self.player.front * self.player.camera_move_speed, self.game_objects)
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.player.move(-self.player.front * self.player.camera_move_speed, self.game_objects)

        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.player.move(-Vector3.cross(self.player.front, self.player.up).normalize() * self.player.camera_move_speed, self.game_objects)
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.player.move(Vector3.cross(self.player.front, self.player.up).normalize() * self.player.camera_move_speed, self.game_objects)

    def add_game_object(self, obj: Actor):
        obj.__setup_vbo__()

        self.game_objects.append(obj)
        self.physics_engine.objects.append(obj)

    def remove_game_object(self, obj: Actor):
        self.game_objects.remove(obj)
        self.physics_engine.objects.remove(obj)

    def add_update_function(self, func):
        self.custom_update_functions.append(func)

    def remove_update_function(self, func):
        self.custom_update_functions.remove(func)

    def add_light(self, light: Light):
        if len(self.lights) < self.max_lights:
            light.setup(GL_LIGHT0 + len(self.lights))
            self.lights.append(light)
            return True
        return False

    def render_3d_scene(self):
        current_time = glfw.get_time()
        dt = current_time - self.last_time
        self.last_time = current_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if self.player:
            self.player.update()

        self.accumulated_time += dt
        while self.accumulated_time >= self.fixed_time_step:
            self.physics_engine.update(dt=self.fixed_time_step)
            self.accumulated_time -= self.fixed_time_step

        for light in self.lights:
            light.update()

        for game_object in self.game_objects:
            game_object.render()

    def render(self):
        while not glfw.window_should_close(self.window) and self.running:
            self._frame_start_time = glfw.get_time()

            glfw.poll_events()
            self.impl.process_inputs()

            for func in self.custom_update_functions:
                func()

            current_time = glfw.get_time()
            self.last_time = current_time

            self.handle_inputs()
            self.render_3d_scene()

            imgui.new_frame()
            self.draw_ui()

            width, height = glfw.get_window_size(self.window)
            self.hud_component.render_all_hud(window_width=width, window_height=height)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

            frame_end_time = glfw.get_time()
            elapsed_time = frame_end_time - self._frame_start_time
            remaining_time = self.frame_time - elapsed_time

            if remaining_time > 0:
                while glfw.get_time() - self._frame_start_time < self.frame_time:
                    pass

        self.cleanup()

    def draw_ui(self):
        pass

    def cleanup(self):
        self.impl.shutdown()
        glfw.terminate()

    def run(self):
        self.render()
