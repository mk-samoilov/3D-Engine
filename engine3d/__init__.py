import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from .core import PygameBasedEngine, ImGUIBasedEngine

Engine = PygameBasedEngine

from .camera import Camera
from .actor import Actor
from .hud import HUD
from .light import Light

from .methods import load_mesh_on_file, load_texture_on_file
