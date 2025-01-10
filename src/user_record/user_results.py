from copy import copy
from src.user_record.user_result_record import UserResultRecord
from src.constants import SAVE_RECORD_PATH

class UserResults:
    def __init__(self, file_path: str = SAVE_RECORD_PATH):
        self.__records: [UserResultRecord] = []
        self.__read_file(file_path)

    def __read_file(self, file_path: str = SAVE_RECORD_PATH):
        with open(file_path, 'r') as f:
            data = f.read().split('\n')
            for record in data:
                if record != "":
                    self.__records.append(UserResultRecord(record))

    def get_top_10(self):
        top_10_records: [UserResultRecord] = copy(self.__records)
        top_10_records.sort()
        top_10_records = top_10_records[:10 if len(self.__records) > 10 else len(self.__records)]

        if len(top_10_records)<10:
            while len(top_10_records)<10:
                top_10_records.append(UserResultRecord("-#0#0"))

        return [(f"{i+1}", f"{top_10_records[i].name}", f"{top_10_records[i].time}", f"{top_10_records[i].score}")
                for i in range(0, 10)]

    @staticmethod
    def save_result(name: str, time: str, score:int):
        with open(SAVE_RECORD_PATH, "a") as file:
            file.write(str(UserResultRecord(f"{name}#{time}#{score}")) + "\n")