class UserResultRecord:
    def __init__(self, data: str):
        data = data.split('#')
        self.__name: str = data[0]
        self.__time: str = data[1]
        self.__score: int = int(data[2])

    def __str__(self) -> str:
        return f"{self.__name}#{self.__time}#{self.__score}"

    @property
    def score(self) -> int:
        return self.__score

    @property
    def name(self) -> str:
        return self.__name

    @property
    def time(self) -> str:
        return self.__time

    def __lt__(self, other) -> bool:
        return self.score > other.score