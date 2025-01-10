import tkinter as tk
from src.constants import BUTTON_TEXT_COLOR, BUTTON_TEXT_COVER, FONT, TAGS

class Buttons:
    @staticmethod
    def create_button(button_name: str, x: float, y: float, master: tk.Canvas, callback: callable):
        button_text = master.create_text(x, y, text=button_name, font=FONT, fill=BUTTON_TEXT_COLOR, tags=TAGS)

        master.tag_bind(button_text, "<Button-1>", lambda e, cmd=callback: cmd())

        master.tag_bind(button_text, "<Enter>",
                        lambda e, t=button_text: master.itemconfig(t, fill=BUTTON_TEXT_COVER))

        master.tag_bind(button_text, "<Leave>",
                        lambda e, t=button_text: master.itemconfig(t, fill=BUTTON_TEXT_COLOR))