import tkinter as tk
from typing import Optional

class Window:
    def __init__(self, root: tk.Tk, bg_path: str):
        self._current_window_frame: Optional[tk.Frame]  = None
        self._root: tk.Tk = root
        self._windows: Optional[dict[str, 'Window']] = None
        self._stretched_image = None
        self._root_width = self._root.winfo_screenwidth()
        self._root_height = self._root.winfo_screenheight()
        self._bg_image = tk.PhotoImage(file=bg_path)
        self._bg_canvas: Optional[tk.Canvas] = None

    @property
    def windows(self) -> dict[str, 'Window']:
        return self._windows

    @windows.setter
    def windows(self, windows: ['Window']):
        self._windows = windows

    @property
    def current_window_frame(self) -> tk.Frame:
        return self._current_window_frame

    @current_window_frame.setter
    def current_window_frame(self, current_window_frame: tk.Frame):
        self._current_window_frame = current_window_frame

    def _clear_current_view(self):
        if self._current_window_frame:
            for widget in self._current_window_frame.winfo_children():
                widget.destroy()
        self._draw_background()

    def show_window(self, **kwargs):
        pass

    def _draw_background(self):
        self._bg_canvas = tk.Canvas(self._current_window_frame, highlightthickness=0)

        self._bg_canvas.pack(fill=tk.BOTH, expand=True)

        canvas_image = self._bg_canvas.create_image(0, 0, image=self._bg_image, anchor='nw')

        self._stretched_image = self._bg_image.subsample(
            self._bg_image.width() // self._root_width,
            self._bg_image.height() // self._root_height
        ) if self._bg_image.width() > self._root_width or self._bg_image.height() > self._root_height else \
            self._bg_image.zoom (
                self._root_width // self._bg_image.width(),
                self._root_height // self._bg_image.height()
            )
        self._bg_canvas.itemconfig(canvas_image, image=self._stretched_image)
        self._bg_canvas.config(width=self._root_width, height=self._root_height)

    def _draw_half_blurred_bg(self, x1, y1, x2, y2, bg_padding=5):
        width = x2 - x1
        height = y2 - y1
        self._bg_canvas.create_rectangle(
            x1 - bg_padding,
            y1 - bg_padding,
            x1 + width + bg_padding,
            y1 + height + bg_padding,
            fill="#4071db",
            outline="white",
            stipple="gray50"
        )
