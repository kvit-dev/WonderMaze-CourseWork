import tkinter as tk
from src.constants import FONT, WIN_FONT, TABLE_FONT
from src.interface.widgets.button import Buttons
from src.interface.windows_class.window import Window
from src.user_record.user_results import UserResults

class WinWindow(Window):
    def show_window(self, **kwargs):
        self._clear_current_view()
        game_time: str = kwargs['game_time']
        score: int = kwargs['score']

        self._bg_canvas.create_text(self._root.winfo_screenwidth() // 2, 150,
                                    text=f"You won!",
                                    font=WIN_FONT, justify="center", fill='pink')

        self._bg_canvas.create_text(self._root.winfo_screenwidth() // 2, 350,
                             text=f"Your score: {score}\n Time: {game_time}\n\nEnter your nickname",
                             font=FONT, justify="center", fill='white')

        name_var = tk.StringVar()
        name_entry = tk.Entry(self._bg_canvas, font=TABLE_FONT, justify="center", textvariable=name_var)

        error_label = None

        def validate_user_input(*args):
            nonlocal error_label
            curr_text = name_var.get()

            if len(curr_text) > 10:
                name_var.set(curr_text[:10])

            if curr_text and error_label:
                self._bg_canvas.delete(error_label)
                error_label = None
                name_entry.config(fg='black')

        name_var.trace('w', validate_user_input)

        self._bg_canvas.create_window(self._root.winfo_screenwidth() // 2, 500, window=name_entry)

        def on_save():
            nonlocal error_label
            if not name_var.get():
                if not error_label:
                    error_label = self._bg_canvas.create_text(
                        self._root.winfo_screenwidth() // 2,
                        550,
                        text="Enter your nickname!",
                        font=FONT,
                        fill='red'
                    )
                name_entry.config(fg='red')
            else:
                UserResults.save_result(name_entry.get(), game_time, score)
                self._windows["Menu"].show_window()

        Buttons.create_button(
            button_name="Save",
            x=self._root.winfo_screenwidth() // 2,
            y=650,
            master=self._bg_canvas,
            callback=on_save
        )