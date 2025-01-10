from typing import Tuple
from src.game.game_entities.cell import Cell

class Maze:
    def __init__(self):
        self.__game_map: [[Cell]] = []
        self.__width: int = 0
        self.__height: int  = 0
        self.__coord_start: Tuple[int,int] = (0, 0)

    def load_game_map(self, file_name:str):
        with open(file_name, "r") as file:
            data:[str] = file.read().split("\n")
            self.__height = int(data.pop(0))
            self.__width = int(data.pop(0))
            for i in range(0, self.__height):
                self.__game_map.append([])
                for j in range(0, self.__width):

                    if len(data) == 0:
                        self.__game_map[i].append(Cell(0, 0, "p"))
                        continue

                    cell_entry = data.pop(0).split(" ")
                    x: int = int(cell_entry[0])
                    y: int = int(cell_entry[1])
                    cell_type: str = cell_entry[2][0]
                    self.__game_map[i].append(Cell(x, y, cell_type))
                    if cell_type == "s":
                        self.__coord_start = (x, y)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def coord_start(self) -> Tuple[int, int]:
        return self.__coord_start

    def get_cell(self, x:int, y:int) -> Cell:
        return self.__game_map[x][y]