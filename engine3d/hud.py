import imgui

class HUDComponent:
    def __init__(self):
        self.elements = []
        self.visible = True

    def add_element(self, element):
        self.elements.append(element)

    def remove_element(self, element):
        if element in self.elements:
            self.elements.remove(element)

    def render_all_hud(self, window_width, window_height):
        if not self.visible:
            return

        for element in self.elements:
            element.render(window_width, window_height)

    def toggle_visibility(self):
        self.visible = not self.visible

class BaseHUDElement:
    def __init__(self, name: str):
        self.name = name
        self.visible = True

    def render(self, window_width, window_height):
        pass

class HUDWindow(BaseHUDElement):
    def __init__(self, name: str, position: tuple = (10, 10), size: tuple = (300, 200), callback=None):
        super().__init__(name)
        self.position = position
        self.size = size
        self.callback = callback

    def render(self, *args):
        if not self.visible:
            return

        imgui.set_next_window_position(*self.position)
        imgui.set_next_window_size(*self.size)
        if imgui.begin(self.name, closable=True):
            if self.callback:
                self.callback()
            else:
                imgui.text(f"Default content for {self.name}")
        imgui.end()
