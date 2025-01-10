from src.interface.widgets.table import Table
from src.interface.widgets.button import Buttons
from src.interface.windows_class.window import Window
from src.constants import TOP_MARGIN, LEFT_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN
from src.user_record.user_results import UserResults

class LeaderBoardWindow(Window):
    def show_window(self, **kwargs):
        self._clear_current_view()

        x1 = LEFT_MARGIN
        y1 = TOP_MARGIN
        x2 = self._bg_canvas.winfo_screenwidth() - RIGHT_MARGIN
        y2 = self._bg_canvas.winfo_screenheight() - BOTTOM_MARGIN
        self._draw_half_blurred_bg(x1, y1, x2, y2)

        user_results = UserResults()
        table = Table(
            screen=self._bg_canvas,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,

            columns={
                "Place" : 0.2,
                "Name" : 0.3,
                "Time": 0.3,
                "Score" : 0.2
            },
            data=user_results.get_top_10(),
            is_line=False,
        )
        table.draw()

        Buttons.create_button(
            button_name="Back To Menu",
            x=self._root.winfo_screenwidth() // 2,
            y = self._root.winfo_screenheight() - BOTTOM_MARGIN / 2,
            master=self._bg_canvas,
            callback=lambda: self._windows["Menu"].show_window()
        )