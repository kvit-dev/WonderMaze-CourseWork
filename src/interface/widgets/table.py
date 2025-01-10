from src.constants import TABLE_HEADERS_COLOR, TABLE_ENTRY_COLOR, FONT, TABLE_FONT

class Table:
    def __init__(self, screen, x1, y1, x2, y2, data, columns, is_line =True):
        self._screen = screen
        self._width = x2 - x1
        self._height = y2 - y1
        self._start_x = x1
        self._start_y = y1
        self.__data = data
        self.__columns = columns
        self.__cell_height = self._height / (len(data) + 1)
        self.__is_line = is_line

        self.__column_width = {}
        for col, proportion in columns.items():
            self.__column_width[col] = self._width * proportion

    def draw(self):
        if self.__is_line:
            self._screen.create_rectangle (
                self._start_x,
                self._start_y,
                self._start_x + self._width,
                self._start_y + self._height,
                fill=""
            )

        self.__draw_headers()
        self.__fill_user_data()

    def __draw_headers(self):
        curr_x = self._start_x

        for col in self.__columns.keys():
            x = curr_x + self.__column_width[col] / 2
            self._screen.create_text(
                x,
                self._start_y + self.__cell_height / 2,
                text=col,
                font = FONT,
                fill = TABLE_HEADERS_COLOR
            )
            curr_x += self.__column_width[col]

    def __fill_user_data(self):
        for row_idx, row_data in enumerate(self.__data):
            curr_x = self._start_x

            for col_idx, cell_data in enumerate(row_data):
                x = curr_x + list(self.__column_width.values())[col_idx] / 2
                y = self._start_y + self.__cell_height * (row_idx + 1.5)

                self._screen.create_text(
                    x,
                    y,
                    text=str(cell_data),
                    font=TABLE_FONT,
                    fill=TABLE_ENTRY_COLOR
                )
                curr_x += list(self.__column_width.values())[col_idx]