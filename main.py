from engine3d import Engine, Actor, load_mesh_on_file, load_texture_on_file

game = Engine()

blue_texture = load_texture_on_file(file="engine3d/exemple_textures/blue_texture.png")
# Don't forget to look at engine3d/exemple_textures/test.png

cube_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cube.json")
cylinder_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cylinder.json")

cube = Actor(position=(0, 0, 0), mesh=cube_mesh, texture=blue_texture, collision=True)
game.add_game_object(cube)

cylinder = Actor(position=(9, 1, -3.25), mesh=cylinder_mesh, texture=blue_texture, collision=True)
game.add_game_object(cylinder)

game.run()
