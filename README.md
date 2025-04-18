# MKE3D off. Documentation (Edition N1 | 18.04.2025)

### Table of Contents:

### Head 1: Engine Components:
#### 1.1. [Engine structure](#engine-structure)
#### 1.2. [Components overview](#components-overview)

### Head 2: Usage Exemple:
#### 2. [Let's create a simple game/simulation](#lets-create-a-simple-game)
#### 2.1. ["We will need"](#we-will-need)
#### 2.2. [Codding the exemple game](#codding)

# Content:

## Engine structure:
```
mke3d
│
├── actor.py
│   └── Actor           # Game object class
│
├── camera.py
│   └── Camera          # Camera class (example usage: as player)
│
├── classes.py          # Various utility classes
│
├── core.py
│   ├── PhysicEngine    # Component/class for handling physics
│   └── Engine3D        # Main engine class
│
├── hud.py              # Heads-up display functionality
│
├── light.py            # Lighting system classes
│
├── meshes.py           # Methods for generate example meshes
│
└── methods.py          # Utility methods
```

## Components Overview:
### 1. core.PhysicEngine

#### Manages physical interactions in the scene, including gravity, collisions, and impulse-based resolution.

    Initializes with a configurable gravity vector and maintains a list of physics-enabled objects.
    Updates object states with gravity application and collision handling over fixed time steps.
    Detects collisions using axis-aligned bounding boxes (AABB) and resolves them with impulses, friction, and penetration correction.

    (File: core.py)

### 2. core.Engine3D

#### The core engine class that orchestrates rendering, input handling, physics simulation, and game object management.

    Sets up the GLFW window, OpenGL context, ImGUI for HUD, and initializes physics and camera systems.
    Processes user inputs (e.g., WASD movement, mouse rotation) and maintains a fixed-timestep physics loop.
    Renders the 3D scene, lights, and HUD while capping the frame rate to a target FPS.

    (File: core.py)

### 3. actor.Actor

#### Represents a 3D object in the scene with physics, rendering, and collision capabilities.

    Initializes with position, rotation, mesh, texture, and physics properties (mass, restitution).
    Renders using OpenGL with vertex buffers for vertices, normals, and UVs.
    Updates position and rotation based on applied forces and impulses, supporting quaternion-based rotation.

    (File: actor.py)

### 4. camera.Camera

#### Controls the player's viewpoint with movement and rotation functionality.

    Provides FPS-style navigation with mouse rotation (yaw/pitch) and WASD movement.
    Updates the view matrix using gluLookAt and prevents movement through colliding objects.
    Configurable with initial position, collision detection, and movement speed.

    (File: camera.py)

### 5. light.Light

#### Defines a light source with ambient, diffuse, and specular components for scene illumination.

    Configures OpenGL lighting with position, color, and attenuation parameters.
    Updates light position dynamically during rendering.

    (File: light.py)

### 6. hud.HUDComponent

#### Manages heads-up display (HUD) elements for the user interface.

    Maintains a list of HUD elements and renders them when visible.
    Provides methods to add/remove elements and toggle visibility.

    (File: hud.py)

### 7. hud.HUDElement

#### HUD class for creating different [drumroll] HUD, using imgui.

    Have a three main porameters: 'visible', 'size', 'position'.

    (File: hud.py)

### classes.Mesh (Utility)

#### Stores 3D model data, including vertices, faces, and UV coordinates.

    Acts as a simple data structure for geometry passed to Actor for rendering and physics.

    (File: classes.py)

### Mesh Generation Functions (Utility, 'meshes' module)

#### Utility methods to procedurally generate example meshes (e.g., cube, sphere).

    gen_cube: Creates a cube mesh with specified dimensions.
    gen_sphere: Generates a sphere mesh with configurable radius and segment count.

    (File: meshes.py)

### Utility Methods ('methods' module)

#### Helper functions for loading assets into the engine.

    load_mesh_on_file: Loads mesh data from a JSON file.
    load_texture_on_file: Loads an image file into an OpenGL texture.

    (File: methods.py)

## Let's create a simple game:
### Let's create a simple game on this engine. Concept: solar system simulation.

### We will need:
### Before we start, download or install the engine. This can be done in two main ways:

#### Way 1: install as a py lib, on PyPi:
```commandline
pip3 install mke3d
```

#### Way 2: download source code (on a GitHub or off. mirror) and install `requirements.txt`.

## Codding:

#### Great, now we're ready to write the game code.

### Let's create config.py for a loading engine:
```python
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "MKE3d Exemple"
WINDOW_ICON = "icon.png"

DRAW_DISTANCE = 1000
MSAA_X = 8
TARGET_FPS = 80
```

### First you need to import the engine components:
```python
from mke3d import Engine3D, Actor, Camera, Light
from mke3d.meshes import gen_sphere
```

### Step 2: init the engine and player object (in exemple: camera):
```python
player = Camera(position=(5, 5, 40), collision=True)
game = Engine3D(player=player)
```

### Step 3: Adding light on scene (optional): 
```python
light = Light(
    position=(0, 0, 0),
    color=(1.0, 1.0, 1.0),
    ambient=2.3,
    diffuse=8000,
    specular=0.5
)
game.add_light(light)
```

### Step 4: Adding the game objects (actors) on scene:
```python
sun_actor = Actor(
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=2, segments=64),
    collision=True
)
game.add_game_object(sun_actor)

small_planet = Actor(
    position=(0, 0, 10),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=56),
    collision=True
)
game.add_game_object(small_planet)
```

### And step 5: Run the engine main loop:
```python
game.run()
```

### Available customizing and improvements:
#### Adding textures on actors:
```python
from mke3d import load_texture_on_file

sun_texture = load_texture_on_file(file="path/to/sun_texture.png")
planet_texture_1 = load_texture_on_file(file="path/to/planet_texture.png")

sun_actor = Actor(
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=2, segments=64),
    texture=sun_texture,
    collision=True
)
game.add_game_object(sun_actor)

small_planet = Actor(
    position=(0, 0, 10),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=56),
    texture=planet_texture_1,
    collision=True
)
game.add_game_object(small_planet)
```

#### Adding planet orbit update function(it need past in front of eng loop run):
```python
import math

orbit_radius = 16
simulation_speed = 1
angle_1 = 0
rotation_angle_1 = 0

def update_planet_orbit():
    global angle_1
    global rotation_angle_1
    angle_1 += simulation_speed / 90
    x = math.cos(angle_1) * orbit_radius
    z = math.sin(angle_1) * orbit_radius
    small_planet.position = Vector3(x, 0, z)

    rotation_angle_1 += simulation_speed
    small_planet.rotation = Vector3(0, rotation_angle_1, 20)

game.add_update_function(func=update_planet_orbit)
```