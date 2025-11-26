from engine3d import Engine3D, Actor, Camera, Light, HUDElement, load_texture_on_file
from engine3d.meshes import gen_sphere

from pygame import Vector3

import math
import imgui


player = Camera((5, 5, 40), collision=True)
game = Engine3D(player=player)

game.update_loading_progress(0.0, "Initializing engine...")


import glfw


class FPSCounter(HUDElement):
    def __init__(self):
        super().__init__(position=(0, 0), size=(80, 40))

        self.fps = 0
        self.frame_count = 0
        self.last_time = glfw.get_time()
        self.update_interval = 0.5

    def update_fps(self):
        current_time = glfw.get_time()
        self.frame_count += 1

        time_elapsed = current_time - self.last_time
        if time_elapsed >= self.update_interval:
            self.fps = int(self.frame_count / time_elapsed)
            self.frame_count = 0
            self.last_time = current_time

    def render(self, window_width, window_height):
        if not self.visible:
            return

        x = window_width - self.size[0]
        y = 10
        imgui.set_next_window_position(x, y)

        if self.visible:
            imgui.begin(
                "FPS",
                flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_ALWAYS_AUTO_RESIZE
            )
            imgui.text(f"FPS: {self.fps}")
            imgui.end()


fps_counter = FPSCounter()


class ControlWindow(HUDElement):
    def __init__(self, fps_counter_ref, game_ref):
        super().__init__(position=(50, 50), size=(486, 340))

        self.show_welcome = True
        self.first_render = True

        self.fps_counter_ref = fps_counter_ref
        self.game_ref = game_ref

        self.window_opened = True

    def render(self, window_width, window_height):
        if not self.visible:
            return
        
        if self.first_render:
            imgui.set_next_window_position(self.position[0], self.position[1], imgui.FIRST_USE_EVER)
            imgui.set_next_window_size(self.size[0], self.size[1], imgui.FIRST_USE_EVER)
            self.first_render = False
        
        flags = (
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_COLLAPSE
        )
        
        opened = [True]
        expanded, opened_state = imgui.begin("MKEngine3D Example", opened, flags)
        
        if not opened_state:
            self.game_ref.running = False
        
        if expanded:
            if self.show_welcome:
                imgui.dummy(0, 10)
                imgui.text("    Welcome from Engine3D Example!")
                imgui.dummy(0, 20)

                imgui.text(" Engine3D supports HUD elements through the HUDComponent")
                imgui.text("system: you can create custom HUD elements by inheriting")
                imgui.text("from HUDElement class, such as this window and FPS counter")

                imgui.dummy(0, 5)

                imgui.text(" Github repo")
                imgui.text("https://github.com/mk-samoilov/3D-Engine")

                imgui.dummy(0, 10)
                imgui.separator()
                imgui.dummy(0, 5)

                imgui.text("Controls:")
                imgui.text("  RMB - Lock/unlock mouse")
                imgui.text("  F1 - Toggle this window")
                imgui.text("  Close window - Exit game")

                imgui.dummy(0, 20)
                
                button_width = 100
                imgui.set_cursor_pos_x((self.size[0] - button_width) / 2)
                
                if imgui.button("Ok", button_width):
                    # imgui.set_next_window_size(180.0, 95.0)
                    self.show_welcome = False
            else:
                imgui.dummy(0, 10)
                
                checked = self.fps_counter_ref.visible
                changed, checked = imgui.checkbox("Show FPS Counter", checked)
                
                if changed:
                    self.fps_counter_ref.visible = checked
            
            imgui.end()


control_window = ControlWindow(fps_counter, game)

game.update_loading_progress(0.2, "Loading assents (assets/textures/sun_texture_v2.png)")
sun_texture = load_texture_on_file(file="assets/textures/sun_texture_v2.png")

game.update_loading_progress(0.3, "Loading assents (assets/textures/earth_planet_texture_v2.png)")
planet_texture_1 = load_texture_on_file(file="assets/textures/earth_planet_texture_v2.png")

game.update_loading_progress(0.3, "Loading assents (assets/textures/mars_planet_texture_v2.png)")
planet_texture_2 = load_texture_on_file(file="assets/textures/mars_planet_texture_v2.png")


game.update_loading_progress(0.5, "Loading scene (lights)")
light = Light(
    position=(0, 0, 0),
    color=(1.0, 1.0, 1.0),
    ambient=2.3,
    diffuse=8000,
    specular=0.5
)
game.add_light(light)

game.update_loading_progress(0.5, "Loading scene (actor sun_actor)")
sun_actor = Actor(
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=3.1, segments=64),
    texture=sun_texture,
    collision=True
)
game.add_game_object(sun_actor)

game.update_loading_progress(0.6, "Loading scene (actor earth_planet)")
earth_planet = Actor(
    position=(0, 0, 16),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=256),
    texture=planet_texture_1,
    collision=True
)
game.add_game_object(earth_planet)

game.update_loading_progress(0.6, "Loading scene (actor mars_planet)")
mars_planet = Actor(
    position=(0, 0, 23),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=1.6, segments=512),
    texture=planet_texture_2,
    collision=True
)
game.add_game_object(mars_planet)

orbit_radius = 16
orbit_radius_2 = 23
simulation_speed = 1
angle_1 = 0
rotation_angle_1 = 0
angle_2 = 11
rotation_angle_2 = 7


def update_fps_counter():
    fps_counter.update_fps()


def update_control_window():
    current_f1_state = glfw.get_key(game.window, glfw.KEY_F1)
    
    if not hasattr(update_control_window, "last_f1_state"):
        update_control_window.last_f1_state = glfw.RELEASE
    
    if current_f1_state == glfw.PRESS and update_control_window.last_f1_state == glfw.RELEASE:
        control_window.visible = not control_window.visible
    
    update_control_window.last_f1_state = current_f1_state


def update_planet_orbit():
    global angle_1
    global rotation_angle_1

    angle_1 += simulation_speed / 90
    x = math.cos(angle_1) * orbit_radius
    z = math.sin(angle_1) * orbit_radius
    earth_planet.position = Vector3(x, 0, z)

    rotation_angle_1 += simulation_speed
    earth_planet.rotation = Vector3(0, rotation_angle_1, 20)

    global angle_2
    global rotation_angle_2

    angle_2 += simulation_speed / 270
    x = math.cos(angle_2) * orbit_radius_2
    z = math.sin(angle_2) * orbit_radius_2
    mars_planet.position = Vector3(x, 0, z)

    rotation_angle_2 += simulation_speed
    mars_planet.rotation = Vector3(0, rotation_angle_2, 20)


game.update_loading_progress(0.75, "Loading engine (registering update functions and hud's)")

game.hud_component.add_element(fps_counter)
game.hud_component.add_element(control_window)

game.add_update_function(func=update_fps_counter)
game.add_update_function(func=update_control_window)
game.add_update_function(func=update_planet_orbit)

game.update_loading_progress(1.0, "Scene loaded")
game.finish_loading()

game.run()
