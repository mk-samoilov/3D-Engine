from engine3d import Engine3D, Actor, Camera, Light, HUDElement, load_texture_on_file
from engine3d.meshes import gen_sphere

from pygame import Vector3

import math
import imgui


player = Camera((5, 5, 40), collision=True)
game = Engine3D(player=player)

# Начальная настройка загрузочного экрана
game.update_loading_progress(0.0, "Инициализация движка...")


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

game.update_loading_progress(0.2, "Loading assents (assets/textures/sun_texture_v2.png)")
sun_texture = load_texture_on_file(file="assets/textures/sun_texture_v2.png")

game.update_loading_progress(0.4, "Loading assents (assets/textures/earth_planet_texture_v2.png)")
planet_texture_1 = load_texture_on_file(file="assets/textures/earth_planet_texture_v2.png")

game.update_loading_progress(0.6, "Loading assents (assets/textures/mars_planet_texture_v2.png)")
planet_texture_2 = load_texture_on_file(file="assets/textures/mars_planet_texture_v2.png")


game.update_loading_progress(0.7, "Loading scene (lights)")
light = Light(
    position=(0, 0, 0),
    color=(1.0, 1.0, 1.0),
    ambient=2.3,
    diffuse=8000,
    specular=0.5
)
game.add_light(light)

game.update_loading_progress(0.8, "Loading scene (actor sun_actor)")
sun_actor = Actor(
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=3.1, segments=64),
    texture=sun_texture,
    collision=True
)
game.add_game_object(sun_actor)

game.update_loading_progress(0.9, "Loading scene (actor earth_planet)")
earth_planet = Actor(
    position=(0, 0, 16),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=256),
    texture=planet_texture_1,
    collision=True
)
game.add_game_object(earth_planet)

game.update_loading_progress(0.9, "Loading scene (actor mars_planet)")
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


game.update_loading_progress(0.8, "Loading engine (registering update functions and hud's)")

game.hud_component.add_element(fps_counter)

game.add_update_function(func=update_fps_counter)
game.add_update_function(func=update_planet_orbit)

game.update_loading_progress(1.0, "Scene loaded")
game.finish_loading()

game.run()
