from src.constants import DIFFICULTY_FONT
from src.interface.windows_class.window import Window
from src.interface.widgets.button import Buttons

class GameSettingWindow(Window):
    def show_window(self, **kwargs):
        self._clear_current_view()

        difficulty: dict[str: [int]] = {
            "Easy": [25, 25, 100],
            "Medium": [35, 35, 250],
            "Hard": [45, 45, 300],
        }
        self._bg_canvas.create_text(self._root.winfo_screenwidth() // 2, 150, text="Choose Difficulty",
                                    font=DIFFICULTY_FONT, fill='white')
        start_y = 350

        for i, (difficulty_name, values) in enumerate(difficulty.items()):
            width, height, score_multiplier = values

            Buttons.create_button(
                button_name=difficulty_name,
                x=self._root.winfo_screenwidth() // 2,
                y=start_y + i * 80,
                master=self._bg_canvas,
                callback=lambda  w=width, h=height, s=score_multiplier: self._windows["Game window"].show_window(width=w, height=h, score_multiplier=s)
            )

        Buttons.create_button(
            button_name="Back To Menu",
            x=self._root.winfo_screenwidth() // 2,
            y=start_y + len(difficulty) * 80 + 40,
            master=self._bg_canvas,
            callback=lambda: self._windows["Menu"].show_window()
        )