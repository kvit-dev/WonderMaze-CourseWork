from src.constants import GAME_NAME_FONT
from src.interface.windows_class.window import Window
from src.interface.widgets.button import Buttons

class MenuWindow(Window):
    def show_window(self, **kwargs):
        self._clear_current_view()

        self._bg_canvas.create_text(self._root.winfo_screenwidth() // 2, 150, text="Wonder Maze", font=GAME_NAME_FONT, fill='white')

        menu_buttons = [
            ("Start Game", lambda: self._windows["Game setting"].show_window()),
            ("Leaderboard", lambda: self._windows["Leader board"].show_window()),
            ("About", lambda: self._windows["About"].show_window()),
            ("Quit", lambda: self._root.quit())
        ]

        start_y = 350
        for i, (button_name, callback) in enumerate(menu_buttons):
            Buttons.create_button(button_name, self._root.winfo_screenwidth() // 2,
                                  start_y + i * 100, self._bg_canvas, callback)