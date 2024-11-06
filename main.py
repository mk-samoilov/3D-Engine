from pygame import Vector3
from engine3d import Engine, Actor, load_mesh_on_file, load_texture_on_file
import math

game = Engine()

blue_texture = load_texture_on_file(file="engine3d/exemple_textures/blue_texture.png")
# Don't forget to look at engine3d/exemple_textures/test.png ))))

cube_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cube.json")
cylinder_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cylinder.json")

cube = Actor(position=(0, 0, 0), mesh=cube_mesh, texture=blue_texture, collision=True)
game.add_game_object(cube)

radius = 6  # Distance from the cube
cylinder = Actor(position=(radius, 1, 0), mesh=cylinder_mesh, texture=blue_texture, collision=True)
game.add_game_object(cylinder)

angle = 0


def update():
    global angle
    angle += 0.02

    new_x = radius * math.cos(angle)
    new_z = radius * math.sin(angle)
    new_position = Vector3((new_x, 1, new_z))

    movement = new_position - cylinder.position
    cylinder.position = new_position

    camera_pos = Vector3(game.camera.position)

    if cylinder.check_collision(camera_pos):
        push_direction = movement.normalize()
        game.camera.position += push_direction * 0.1


game.connect_update_function(func=update)
game.run()
