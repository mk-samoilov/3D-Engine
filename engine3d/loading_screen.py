import imgui


class LoadingScreen:
    def __init__(self):
        self.progress = 0.0
        self.status_text = "Loading..."
        self.visible = True
    
    def set_progress(self, progress: float):
        self.progress = max(0.0, min(1.0, progress))
    
    def set_status(self, text: str):
        self.status_text = text
    
    def render(self, window_width: int, window_height: int):
        if not self.visible:
            return

        window_size = (400, 150)
        pos_x = (window_width - window_size[0]) / 2
        pos_y = (window_height - window_size[1]) / 2
        
        imgui.set_next_window_position(pos_x, pos_y)
        imgui.set_next_window_size(window_size[0], window_size[1])

        flags = (
            imgui.WINDOW_NO_TITLE_BAR |
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_MOVE |
            imgui.WINDOW_NO_SCROLLBAR |
            imgui.WINDOW_NO_COLLAPSE |
            imgui.WINDOW_ALWAYS_AUTO_RESIZE
        )
        
        imgui.begin("Loading", flags=flags)

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 15))

        text_width = imgui.calc_text_size(self.status_text).x
        imgui.set_cursor_pos_x((window_size[0] - text_width) / 2)
        imgui.text(self.status_text)
        
        imgui.pop_style_var()

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 10))
        
        progress_text = f"{int(self.progress * 100)}%"
        imgui.progress_bar(self.progress, (window_size[0] - 40, 0), progress_text)
        
        imgui.pop_style_var()
        
        imgui.end()
    
    def hide(self):
        self.visible = False
    
    def show(self):
        self.visible = True

