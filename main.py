from engine3d import Engine, Actor, Camera, HUD, Light, load_texture_on_file
from engine3d.meshes import gen_sphere
from pygame import Vector3
import math

player = Camera((5, 5, 40), collision=True)
game = Engine(player=player)

blue_texture = load_texture_on_file(file="engine3d/exemple_textures/sun_texture.png")
planet_texture_1 = load_texture_on_file(file="engine3d/exemple_textures/planet_texture_1.png")

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
    mesh=gen_sphere(radius=3.1, segments=32),
    texture=blue_texture,
    collision=True
)
game.add_game_object(sun_actor)

small_planet = Actor(
    position=(0, 0, 16),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=32),
    texture=planet_texture_1,
    collision=True
)
game.add_game_object(small_planet)

orbit_radius = 16
simulating_speed = 1
angle = 0
rotation_angle = 0

def update_planet_orbit():
    global angle
    global rotation_angle
    angle += simulating_speed / 170
    x = math.cos(angle) * orbit_radius
    z = math.sin(angle) * orbit_radius
    small_planet.position = Vector3(x, 0, z)

    rotation_angle += simulating_speed
    small_planet.rotation = Vector3(0, rotation_angle, 20)

def update_fps_hud():
    hud = HUD(
        font_class=game.fonts.default,
        text=f"FPS: {game.clock.get_fps():.1f}",
        color=(255, 255, 255),
        position=(200, 150)
    )
    game.hud_component.update_hud(uuid="FPS_HUD", hud=hud)

def update_player_pos_hud():
    hud = HUD(
        font_class=game.fonts.default_2,
        text=f"Player pos: {player.position}",
        color=(255, 255, 255),
        position=(200, 170)
    )
    game.hud_component.update_hud(uuid="PLAYER_POS_HUD", hud=hud)

game.add_update_function(func=update_planet_orbit)
game.add_update_function(func=update_player_pos_hud)
game.add_update_function(func=update_fps_hud)

game.run()
