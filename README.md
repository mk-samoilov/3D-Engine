# 3D Game Engine Library

<img src="./engine3d/engine-icon.png" width="150">

#### This is a simple 3D game engine built with Python, Pygame, and OpenGL. It provides a basic framework for creating 3D games and applications.

<img src="./screenshot.png" width="670">

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Structure](#structure)
4. [Main Components](#main-components)
5. [Usage](#usage)
6. [Example](#example)

## Features

- 3D rendering with OpenGL
- Camera system with collision detection
- Actor/GameObject system
- Mesh loading from JSON files
- Texture mapping support
- Basic collision detection
- Basic physical system
- Basic lighting system
- Event handling system

## Installation

To use this 3D game engine, you need to have the following dependencies installed:

- Python 3.x
- Pygame
- NumPy
- PyOpenGL
- Pillow

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
- `methods.py`: Contains function `load_mesh_on_file` and `load_texture_on_file`.

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

Here's a simple example that loads and displays a cube and cylinder:

```python
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
```

This example initializes the engine, loads a cube mesh, creates an actor with the mesh, adds it to the engine, and starts the game loop.

Controls:
- Use W, A, S, D to move the camera
- Right-click and drag to rotate the camera
- Close the window to exit

With this engine, you can create simple 3D environments and games. Extend the `Actor` class to add more functionality to your game objects, or modify the `Engine` class to add more features to your game loop.
