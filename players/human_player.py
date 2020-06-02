"""Plik zawierający klasę gracza"""

from utils import players_utils
from utils.constants import Basic
from utils.constants import GameStatus


class HumanPlayer:
    """Klasa obsługująca gracza rzeczywistego."""

    def __init__(self, board, levels, player_number):
        """Konstruktor przyjmujący podstawowe dane do późniejszych obliczeń."""
        self.board = board
        self.levels = levels
        self.type_of_player = Basic.HUMAN

        self.player_number = player_number

        # po tym numerze identyfikujemy gracza, ale nie można wypisać drugiego gracza jako -1

        if player_number < 0:
            player_number = 2

        self.begin_info = f"Zaczyna gracz numer {player_number}"
        self.turn_info = f"Tura gracza numer {player_number}"
        self.end_info = f"Wygrał gracz numer {player_number}"

    def make_move(self, col, sign):
        """Metoda wywołana po wybraniu kolumny przez gracza

        Sprawdza czy w danej kolumnie mozna umieścić monetę,
        następnie przeprowadza test na zwycięstwo"""
        row = self.levels[col]
        if row < 0:
            return GameStatus.COLUMN_FULL

        self.board[row][col] = sign * Basic.COIN

        status = players_utils.check(self.board, row, col, sign * Basic.COIN)
        if status:
            return GameStatus.WON

        self.levels[col] -= 1

        return GameStatus.COLUMN_NOT_FULL
