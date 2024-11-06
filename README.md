# 3D Game Engine Library

This is a simple 3D game engine built with Python, Pygame, and OpenGL. It provides a basic framework for creating 3D games and applications.

## Table of Contents

1. [Installation](#installation)
2. [Structure](#structure)
3. [Main Components](#main-components)
4. [Usage](#usage)
5. [Example](#example)

## Installation

To use this 3D game engine, you need to have the following dependencies installed:

- Python 3.x
- Pygame
- NumPy
- PyOpenGL

You can install these dependencies using pip:

```
pip install pygame numpy PyOpenGL Pillow
```
Or
```
pip install -r requirements.txt
```

## Structure

The engine is organized into several modules:

- `core.py`: Contains the main `Engine` class that handles the game loop and OpenGL setup.
- `camera.py`: Implements the `Camera` class for 3D navigation.
- `actor.py`: Defines the `Actor` class for game objects.
- `mesh.py`: Contains the `Mesh` class for storing 3D model data.
- `dt.py`: Implements a `DataTable` class for storing additional data.
- `methods.py`: Provides utility functions like `load_mesh_on_file`.

## Main Components

### Engine

The `Engine` class is the core of the game engine. It handles:

- Initializing Pygame and OpenGL
- Managing the game loop
- Handling user input
- Updating and rendering game objects

### Camera

The `Camera` class manages the 3D view. It supports:

- Camera movement (WASD keys)
- Camera rotation (mouse input)

### Actor

The `Actor` class represents game objects in the 3D world. It:

- Stores position and mesh data
- Handles rendering of the object

### Mesh

The `Mesh` class stores the vertex and face data for 3D models.

## Usage

To use the engine, follow these steps:

1. Create an instance of the `Engine` class.
2. Load 3D models using `load_mesh_on_file`.
3. Create `Actor` instances with the loaded meshes.
4. Add the actors to the engine using `add_game_object`.
5. Call the `run` method on the engine to start the game loop.

## Example

Here's a simple example that loads and displays a cube:

```python
from engine3d import Engine, Actor, load_mesh_on_file, load_texture_on_file

game = Engine()

cube_texture = load_texture_on_file(file="engine3d/exemple_textures/blue_texture.png")
cube_mesh = load_mesh_on_file(file="engine3d/exemple_meshes/cube.json")

cube = Actor(position=(0, 0, 0), mesh=cube_mesh, texture=cube_texture)
game.add_game_object(cube)

cube = Actor(position=(9, 1, -3.25), mesh=cube_mesh, texture=cube_texture)
game.add_game_object(cube)

game.run()
```

This example initializes the engine, loads a cube mesh, creates an actor with the mesh, adds it to the engine, and starts the game loop.

Controls:
- Use W, A, S, D to move the camera
- Right-click and drag to rotate the camera
- Close the window to exit

With this engine, you can create simple 3D environments and games. Extend the `Actor` class to add more functionality to your game objects, or modify the `Engine` class to add more features to your game loop.