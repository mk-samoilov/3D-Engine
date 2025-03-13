from engine3d import Engine, Actor, Camera, HUD, load_mesh_on_file, load_texture_on_file
from engine3d.meshes import gen_cube

from pygame import Vector3

player = Camera((0, 0, 12), collision=True)
game = Engine(player=player)

blue_texture = load_texture_on_file(file="engine3d/exemple_textures/blue_texture.png")
# Don't forget to look at engine3d/exemple_textures/test.png ))))

cube_mesh = gen_cube(width=1, height=1, depth=1)
cylinder_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cylinder.json")

cube = Actor(position=(0, 0, 0), rotation=(0, 0, 0), mesh=cube_mesh, texture=blue_texture, collision=True, physic=True, mass=2.5)
game.add_game_object(cube)

cube_2 = Actor(position=(0, 7, 0), rotation=(0, 0, 0), mesh=cube_mesh, texture=blue_texture, collision=True, physic=True)
game.add_game_object(cube_2)

angle = 0

cube.apply_force(force=Vector3(0, 100, 0))
cube_2.apply_force(force=Vector3(0, -100, 0))

def update_fps_hud():
    hud = HUD(
        font_class=game.default_font,
        text=f"FPS: {game.clock.get_fps():.1f}",
        color=(255, 255, 255),
        position=(200, 150)
    )
    game.hud_component.update_hud(uuid="FPS_HUD", hud=hud)

game.add_update_function(func=update_fps_hud)
game.run()
