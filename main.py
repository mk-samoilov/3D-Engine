from engine3d import Engine, Actor, load_mesh_on_file

game = Engine()

cube_mesh = load_mesh_on_file("engine3d/exemple_meshes/cube.json")

cube = Actor(position=(0, 0, 0), mesh=cube_mesh)
game.add_game_object(cube)

game.run()
