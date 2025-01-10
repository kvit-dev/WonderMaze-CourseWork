import tkinter as tk

from src.constants import BOTTOM_MARGIN, TOP_MARGIN, LEFT_MARGIN, RIGHT_MARGIN, \
    ABOUT_TITLE_FONT, ABOUT_TEXT_FONT, KEYBOARD_KEYS
from src.interface.widgets.button import Buttons
from src.interface.windows_class.window import Window

ABOUT_IMG_WIDTH = 300
ABOUT_IMG_HEIGHT = 150

class AboutGame(Window):
    def show_window(self, *args):
        self._clear_current_view()
        x1 = LEFT_MARGIN
        y1 = TOP_MARGIN
        x2 = self._bg_canvas.winfo_screenwidth() - RIGHT_MARGIN
        y2 = self._bg_canvas.winfo_screenheight() - BOTTOM_MARGIN
        self._draw_half_blurred_bg(x1, y1, x2, y2)

        title = "Hey there! Welcome to Wonder Maze"

        description = (
            "Labyrinths are a fascinating type of puzzle, and they present a different type of challenge to the brain.\n\n"
            "Neuropsychobiological studies show that solving mazes activates a network in the brain from the visual "
            "to the parietal areas.\n\n"
            "So it is not only interesting and fun, but also useful.\n\n\n"
            "\t\tHow to play?\n"
            "The “player” is controlled by the keys up, left, right, down.\n"
            "If you need to return to main menu press 'Esc'\n\n"
        )
        footer = "Have fun and reach the top!"

        self._bg_canvas.create_text(
            (x1 + x2) / 2, y1 + 30,
            text=title,
            font=ABOUT_TITLE_FONT,
            fill="white",
            anchor="n"
        )

        self._bg_canvas.create_text(
            (x1 + x2) / 2, y1 + 100,
            text=description,
            font=ABOUT_TEXT_FONT,
            fill="black",
            width=x2 - x1 - 40,
            anchor="n"
        )

        self._img = tk.PhotoImage(file=KEYBOARD_KEYS)
        self._img = self._img.subsample(
            self._img.width() // ABOUT_IMG_WIDTH,
            self._img.height() // ABOUT_IMG_HEIGHT
        ) if self._img.width() > ABOUT_IMG_WIDTH or self._img.height() > ABOUT_IMG_HEIGHT else \
                self._img.zoom(
                    ABOUT_IMG_WIDTH // self._img.width(),
                    ABOUT_IMG_HEIGHT // self._img.height()
                )

        self._bg_canvas.create_image(
            (x1 + x2) / 2, y1 + 515,
            image=self._img,
            anchor="n"
        )

        self._bg_canvas.create_text(
            (x1 + x2) / 2, y1 + 700,
            text=footer,
            font=ABOUT_TEXT_FONT,
            fill="white",
            width=x2 - x1 - 40,
            anchor="n"
        )

        Buttons.create_button(
            button_name="Back To Menu",
            x=self._root.winfo_screenwidth() // 2,
            y=self._root.winfo_screenheight() - BOTTOM_MARGIN / 2,
            master=self._bg_canvas,
            callback=lambda: self._windows["Menu"].show_window()
        )