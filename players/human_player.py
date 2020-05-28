"""Plik zawierający klasę gracza"""

import utils.players_utils as pu

from utils.constans import GameStatus, Basic


class HumanPlayer:
    """Klasa obsługująca gracza rzeczywistego."""

    def __init__(self, board, levels):
        """Konstruktor przyjmujący podstawowe dane do późniejszych obliczeń."""
        self.board = board
        self.levels = levels

    def make_move(self, col, sign):
        """Metoda wywołana po wybraniu kolumny przez gracza

        Sprawdza czy w danej kolumnie mozna umieścić monetę,
        następnie przeprowadza test na zwycięstwo"""
        row = self.levels[col]
        if row < 0:
            self.set_stat("Brak miejsca w tej kolumnie, strzel ponownie...")
            return GameStatus.COLUMN_FULL

        self.board[row][col] = sign * Basic.COIN

        status = pu.check(self.board, row, col, sign * Basic.COIN)
        if status:
            return GameStatus.WON

        self.levels[col] -= 1

        return GameStatus.COLUMN_NOT_FULL
