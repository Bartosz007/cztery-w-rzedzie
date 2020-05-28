"""Plik zawierający klasę, obsługującą gracza komputerowego."""

import utils.players_utils as pu
from utils.constans import Basic, GameStatus

INF = 99999999999999


class ComputerPlayer:
    """Klasa obsługująca gracza komputerowego."""

    def __init__(self, board, levels, difficulty):
        """Konstruktor przyjmujący podstawowe dane do późnijeszych obliczeń."""
        self.board = board
        self.levels = levels
        self.difficulty = difficulty

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
        c_board = [[self.board[row][col] for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        c_levels = [self.levels[x] for x in range(Basic.COLS)]

        fields = pu.right_fields(c_levels)
        col = 0
        if self.difficulty == 0:
            col = pu.random_field(fields)
        else:
            col = pu.minimax(c_board, c_levels, self.difficulty, True)[0]

        row = self.levels[col]

        self.board[row][col] = -Basic.COIN

        status = pu.check(self.board, row, col, -Basic.COIN)
        if status:
            return GameStatus.WON

        self.levels[col] -= 1
        return GameStatus.COLUMN_NOT_FULL
