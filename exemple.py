from engine3d import Engine3D, Actor, Camera, Light, HUDWindow, load_texture_on_file
from engine3d.meshes import gen_sphere

from pygame import Vector3

import math
import imgui

player = Camera((5, 5, 40), collision=True)
game = Engine3D(player=player)

import glfw

class FPSCounter(HUDWindow):
    def __init__(self):
        super().__init__()

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

    def render(self, *args):
        imgui.set_next_window_position(*self.position)
        if self.visible:
            imgui.begin(
                "FPS",
                flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_ALWAYS_AUTO_RESIZE
            )
            imgui.text(f"FPS: {self.fps}")
            imgui.end()

fps_counter = FPSCounter()

blue_texture = load_texture_on_file(file="exemple_textures/sun_texture.png")
planet_texture_1 = load_texture_on_file(file="exemple_textures/planet_texture_1.png")
planet_texture_2 = load_texture_on_file(file="exemple_textures/planet_texture_2.png")

light = Light(
    position=(0, 0, 0),
    color=(1.0, 1.0, 1.0),
    ambient=2.3,
    diffuse=8000,
    specular=0.5
)
game.add_light(light)

sun_actor = Actor(
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=3.1, segments=64),
    texture=blue_texture,
    collision=True
)
game.add_game_object(sun_actor)

small_planet = Actor(
    position=(0, 0, 16),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=128),
    texture=planet_texture_1,
    collision=True
)
game.add_game_object(small_planet)

big_planet = Actor(
    position=(0, 0, 23),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=1.6, segments=256),
    texture=planet_texture_2,
    collision=True
)
game.add_game_object(big_planet)

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
    small_planet.position = Vector3(x, 0, z)

    rotation_angle_1 += simulation_speed
    small_planet.rotation = Vector3(0, rotation_angle_1, 20)

    global angle_2
    global rotation_angle_2
    angle_2 += simulation_speed / 270
    x = math.cos(angle_2) * orbit_radius_2
    z = math.sin(angle_2) * orbit_radius_2
    big_planet.position = Vector3(x, 0, z)

    rotation_angle_2 += simulation_speed
    big_planet.rotation = Vector3(0, rotation_angle_2, 20)

game.hud_component.add_element(fps_counter)

game.add_update_function(func=update_fps_counter)
game.add_update_function(func=update_planet_orbit)

game.run()
