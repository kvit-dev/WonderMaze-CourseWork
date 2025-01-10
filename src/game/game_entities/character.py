from typing import Tuple

class Character:
    def __init__(self):
        self._x:int = 0
        self._y:int = 0

    def get_coord(self) -> Tuple[int, int]:
        return self._x, self._y

    def set_coord(self, coord: Tuple[int, int]):
        self._x, self._y  = coord

    def move(self, direction: str):
        match direction:
            case "up":
                self._y+=1
            case "down":
                self._y-=1
            case "left":
                self._x-=1
            case "right":
                self._x+=1
            case _:
                pass