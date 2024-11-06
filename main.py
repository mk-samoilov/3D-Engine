from engine3d import Engine, Actor, load_mesh_on_file, load_texture_on_file

game = Engine()

cube_texture = load_texture_on_file(file="engine3d/exemple_textures/blue_texture.png")
cube_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cube.json")

cube = Actor(position=(0, 0, 0), mesh=cube_mesh, texture=cube_texture)
game.add_game_object(cube)

cylinder_texture = load_texture_on_file(file="engine3d/exemple_textures/blue_texture.png")
cylinder_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cylinder.json")

cylinder = Actor(position=(9, 1, -3.25), mesh=cylinder_mesh, texture=cylinder_texture)
game.add_game_object(cylinder)

game.run()
