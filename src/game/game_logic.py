import time
import ctypes
from .game_entities.maze import Maze
from .game_entities.player import Player
from .game_entities.cell import CellType
from typing import Tuple
from src.constants import MAZE_MAP_FILE, MAZE_CONFIG_MAP, MAZE_GENERATOR_LIB

class GameLogic:
    def __init__(self, width: int, height: int, score_multiplier: int):
        self.__maze: Maze = Maze()
        self.__generate_maze(width, height)
        self.__player: Player = Player()
        self.__player.set_coord(self.__maze.coord_start)
        self.__score_multiplier: int = score_multiplier
        self.__start_time: float = time.time()

    @property
    def maze(self) -> Maze:
        return self.__maze

    @property
    def player(self) -> Player:
        return self.__player

    def __get_game_time(self):
        return int(time.time() - self.__start_time)

    def move_player(self, direction: str):
        player_current_x: int
        player_current_y: int

        player_current_x, player_current_y = self.__player.get_coord()
        match direction:
            case 'up'   : new_coord: Tuple[int, int] = (player_current_x, player_current_y+1)
            case 'down' : new_coord: Tuple[int, int] = (player_current_x, player_current_y-1)
            case 'left' : new_coord: Tuple[int, int] = (player_current_x-1, player_current_y)
            case 'right': new_coord: Tuple[int, int] = (player_current_x+1, player_current_y)
            case _      : new_coord: Tuple[int, int] = (player_current_x, player_current_y)

        new_x:int
        new_y:int
        new_x, new_y = new_coord

        if not self.__out_of_bounds(new_coord) and self.__maze.get_cell(new_x, new_y).type !=CellType.WALL.value:
            self.__player.move(direction)

    def __out_of_bounds(self, coord: Tuple[int, int]) -> bool:
        if coord[0] < 0 or coord[0] > self.__maze.width-1 or coord[1] < 0 or coord[1] > self.__maze.height - 1:
            return True
        return False

    def is_win(self) -> bool:
        x, y = self.__player.get_coord()
        return self.__maze.get_cell(x,y).type == CellType.FINISH.value

    def __generate_maze(self, width: int, height: int):
        with open(MAZE_CONFIG_MAP, "w") as f:
            f.write(f"{width} {height}")

        try:
            maze_lib = ctypes.CDLL(MAZE_GENERATOR_LIB)

            maze_lib.Maze_new.argtypes = [ctypes.c_char_p]
            maze_lib.Maze_new.restype = ctypes.c_void_p

            maze_lib.Maze_saveMazeToFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            maze_lib.Maze_saveMazeToFile.restype = None

            maze = maze_lib.Maze_new(MAZE_CONFIG_MAP.encode('utf-8'))

            maze_lib.Maze_saveMazeToFile(maze, MAZE_MAP_FILE.encode('utf-8'))

            self.__maze.load_game_map(MAZE_MAP_FILE)

            maze_lib.Maze_delete.argtypes = [ctypes.c_void_p]
            maze_lib.Maze_delete.restype = None

        except Exception as e:
            print(f"Error in method: {e}")
            raise

    def get_score(self) -> int:
        elapsed_time: int = self.__get_game_time()
        score: int = int((self.__score_multiplier * self.__maze.width * self.__maze.height) / elapsed_time
                         if elapsed_time > 0 else 1)
        return score

    def get_formatted_time(self) -> str:
        seconds: int = self.__get_game_time()
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
