from src.game.game_logic import GameLogic
from src.interface.windows_class.window import Window
from src.game.rendering import GameRender

class GameWindow(Window):
    def show_window(self, **kwargs):
        width = kwargs["width"]
        height = kwargs["height"]
        score_multiplier = kwargs["score_multiplier"]
        self._clear_current_view()

        game_logic: GameLogic = GameLogic(width, height, score_multiplier)
        rendering: GameRender = GameRender(game_logic, self._current_window_frame, self._root, self._bg_canvas)
        rendering.start_loop()

        if game_logic.is_win():
            game_time: str = game_logic.get_formatted_time()
            score: int = game_logic.get_score()
            self._windows["Win window"].show_window(game_time = game_time, score = score)