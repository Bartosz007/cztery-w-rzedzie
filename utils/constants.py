"""Plik klas ze stałymi"""


class GameStatus:
    """Stałe dotyczące wyniku gry"""
    COLUMN_FULL = 0
    COLUMN_NOT_FULL = 1
    STILL_IN_GAME = 2
    DRAW = 3
    WON = 7


class Style:
    """Stałe dotyczące wyglądu"""
    BACKGROUND_COLOR = "#296380"
    BUTTON_COLOR = "#D15304"

    CANVAS_BACKGROUND = "#8A3500"
    DEFAULT_COIN_COLOR = "white"

    PLAYER_ONE_COLOR = "#FF2200"
    PLAYER_TWO_COLOR = "#FF9B21"

    FONT = "Times New Roman"
    FONT_SIZE = 15


class Basic:
    """Podstawowe stałe gry"""
    NUM_COLUMNS = 7
    NUM_ROWS = 6
    COIN = 1

    DEFAULT_POSITION = 5
    EMPTY_POSITION = 0

    HUMAN = 0
    COMPUTER = 1

    PLAYER_ONE = 1
    PLAYER_TWO = -1
