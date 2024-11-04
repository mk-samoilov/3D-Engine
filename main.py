from engine3d import Engine, Actor

engine = Engine(800, 600)

cube_vertices = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
]
cube_faces = [
    (0, 1, 2), (2, 3, 0),
    (1, 5, 6), (6, 2, 1),
    (5, 4, 7), (7, 6, 5),
    (4, 0, 3), (3, 7, 4),
    (3, 2, 6), (6, 7, 3),
    (4, 5, 1), (1, 0, 4)
]
cube = Actor((0, 0, 0), cube_vertices, cube_faces)
engine.add_game_object(cube)

engine.run()
