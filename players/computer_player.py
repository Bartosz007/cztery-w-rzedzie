"""Plik zawierający klasę, obsługującą gracza komputerowego."""

from utils import players_utils
from utils.constants import Basic
from utils.constants import GameStatus


INF = 99999999999999


class ComputerPlayer:
    """Klasa obsługująca gracza komputerowego."""

    def __init__(self, board, levels, player_number, difficulty):
        """Konstruktor przyjmujący podstawowe dane do późnijeszych obliczeń."""
        self.board = board
        self.levels = levels
        self.difficulty = difficulty
        self.type_of_player = Basic.COMPUTER

        self.player_number = player_number
        self.begin_info = "Zaczyna komputer"
        self.turn_info = "Tura komputera"
        self.end_info = "Wygrał komputer"

    def change_difficulty(self, difficulty):
        """Odpowiada za zmianę poziomu umiejętności gracza komputerowego."""
        self.difficulty = difficulty

    #  print(difficulty)

    def make_move(self, _, __):  # ani kolumna ani znak nie są wazne
        """Metoda wykonująca strzał gracza komputerowego

        Oblicza pola w które można strzelić,
        nastepnie algorytmem minimax wybiera najoptymalniejsze pole.
        Wykonuje również test na zwycięstwo."""

        # kopiowanie planszy do późnijeszych obliczeń
        c_board, c_levels = players_utils.copy_data(self.board, self.levels)
        fields = players_utils.right_fields(c_levels)

        if self.difficulty == 0:
            col = players_utils.random_field(fields)
        else:
            col = players_utils.minimax(c_board, c_levels, self.difficulty, True)[0]

        row = self.levels[col]

        self.board[row][col] = -Basic.COIN

        status = players_utils.check(self.board, row, col, -Basic.COIN)
        if status:
            return GameStatus.WON

        self.levels[col] -= 1
        return GameStatus.COLUMN_NOT_FULL
