import time
import tkinter as tk
from src.game.game_entities.cell import Cell, CellColor, CellType
from src.game.game_logic import GameLogic
from src.constants import OUTLINE_COLOR, PLAYER_COLOR, FPS, FONT, PADDING, TIMER_COLOR

class GameRender:
    def __init__(self, game_logic: GameLogic, window: tk.Frame, root: tk.Tk, bg_canvas: tk.Canvas):
        self.__window = window
        self.__game_logic = game_logic
        self.__offset_x: int = 0
        self.__offset_y: int = 0
        self.__cell_size: int = 0
        self.__root: tk.Tk = root
        self.__bg_canvas: tk.Canvas = bg_canvas

        self.__screen = tk.Canvas(self.__bg_canvas, width=root.winfo_height(), height=root.winfo_height(),
                                  bg=CellColor.WALL.value, highlightthickness=0)
        self.__bg_canvas.create_window(
            self.__bg_canvas.winfo_screenwidth() // 2,
            self.__bg_canvas.winfo_screenheight() // 2,
            window=self.__screen
        )
        self.__time_label = self.__bg_canvas.create_text(150, 50, text="00:00:00", font=FONT, fill=TIMER_COLOR, tags="time label")

    def __add_event_handle(self):
        up_button_move: [str] = ["w", "up"]
        left_button_move: [str] = ["a", "left"]
        right_button_move: [str] = ["d", "right"]
        down_button_move: [str] = ["s", "down"]

        def handle_key_press(event):
            key: str = event.keysym.lower()
            if key in up_button_move:
                self.__game_logic.move_player('up')
            elif key in left_button_move:
                self.__game_logic.move_player('left')
            elif key in down_button_move:
                self.__game_logic.move_player('down')
            elif key in right_button_move:
                self.__game_logic.move_player('right')
            self.__draw_player()

        self.__root.bind("<KeyPress>", handle_key_press)

    def __draw_player(self):
        current_player_x, current_player_y = self.__game_logic.player.get_coord()
        self.__draw_rect(current_player_x, current_player_y, PLAYER_COLOR)

        old_player_x, old_player_y = self.__game_logic.player.get_old_coord()
        if old_player_x is not None:
            self.__draw_rect(old_player_x, old_player_y, CellColor.PASS.value)

    def __draw_maze(self):
        self.__screen.delete("all")

        for x in range(self.__game_logic.maze.width):
            for y in range(self.__game_logic.maze.height):
                cell: Cell = self.__game_logic.maze.get_cell(x, y)
                match cell.type:
                    case CellType.PASS.value:
                        color: str = CellColor.PASS.value
                    case CellType.WALL.value:
                        color: str = CellColor.WALL.value
                    case CellType.FINISH.value:
                        color: str = CellColor.FINISH.value
                    case _:
                        color: str = CellColor.DEFAULT.value
                self.__draw_rect(x, y, color)
        self.__screen.update()

    def __calc_game_session_values(self):
        self.__screen.update()

        maze_width: int = self.__game_logic.maze.width
        maze_height: int = self.__game_logic.maze.height

        screen_width: int = self.__screen.winfo_width() - (2 * PADDING)
        screen_height: int = self.__screen.winfo_height() - (2 * PADDING)

        width_cell_size = screen_width / maze_width
        height_cell_size = screen_height / maze_height

        self.__cell_size: float = min(width_cell_size, height_cell_size)

        total_maze_width: float = self.__cell_size * maze_width
        total_maze_height: float = self.__cell_size * maze_height

        self.__offset_x: float = (self.__screen.winfo_width() - total_maze_width) / 2
        self.__offset_y: float = (self.__screen.winfo_height() - total_maze_height) / 2

        self.__screen.config(
            width=total_maze_width + (2 * PADDING),
            height=total_maze_height + (2 * PADDING)
        )

    def render(self):
        self.__update_time_label()
        self.__screen.update()

    def start_loop(self):
        self.__calc_game_session_values()
        self.__add_event_handle()
        self.__draw_maze()
        self.__draw_player()
        sleep_time: float = 1 / FPS
        while not self.__game_logic.is_win():
            try:
                time.sleep(sleep_time)
                self.render()
            except Exception as e:
                break

        self.__root.unbind("<KeyPress>")

    def __draw_rect(self, x: int, y: int, bg_color: str):
        x1: int = self.__offset_x + x * self.__cell_size
        y1: int = self.__offset_y + (self.__game_logic.maze.width - 1 - y) * self.__cell_size
        x2: int = x1 + self.__cell_size
        y2: int = y1 + self.__cell_size
        self.__screen.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=OUTLINE_COLOR)

    def __update_time_label(self):
        self.__bg_canvas.itemconfig(self.__time_label, text=self.__game_logic.get_formatted_time())