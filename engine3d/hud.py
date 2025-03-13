from typing import Tuple

import pygame
from pygame.font import Font

from OpenGL.GL import *

class HUD:
    def __init__(self, font_class: Font, text: str, position: Tuple[int, int], color: Tuple[int, int, int]):
        self.font_class = font_class
        self.text = str(text)
        self.position = position
        self.text_color = color

class HUDComponent:
    def __init__(self):
        self.hud_elements = {}

    def update_hud(self, uuid: str, hud: HUD):
        self.hud_elements[uuid] = hud

    def del_hud(self, uuid: str):
        if uuid in self.hud_elements:
            del self.hud_elements[uuid]

    def render_all_hud(self, window_width: int, window_height: int):
        window_width = int(window_width)
        window_height = int(window_height)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, window_width, 0, window_height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)

        for element in self.hud_elements.values():
            text_surface = element.font_class.render(element.text, True, element.text_color)
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            glRasterPos2f(element.position[0], window_height - element.position[1])
            glDrawPixels(
                text_surface.get_width(),
                text_surface.get_height(),
                GL_RGBA, GL_UNSIGNED_BYTE, text_data
            )

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
