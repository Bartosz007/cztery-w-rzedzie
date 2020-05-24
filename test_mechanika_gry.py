"""Plik z klasą testującą metody gry z klasy GameFunctions"""

import unittest

from mechanika_gry import GameFunctions
from okno_gry import ConnectFour

COLS = 7
ROWS = 6


class Tests(unittest.TestCase):
    """Klasa testująca metody z klasy GameFunctions"""
    def test_two_shots(self):
        """Test wykonujący po dwa strzały każdym kolorem monety

        Powinny zostać wrzucone i spać na dół pola gry,
        lub zatrzymać się na już wrzuconej monecie"""

        compare_table = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0, 0]]
        tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        tlevels = [5 for col in range(COLS)]
        game_functions = GameFunctions(None, None, ConnectFour.end_game,
                                       tpoles, tlevels, False, None, None)
        game_functions.calculate(1)
        game_functions.calculate(2)
        game_functions.calculate(1)
        game_functions.calculate(2)
        game_functions.calculate(1)
        self.assertEqual(game_functions.tpoles, compare_table)

    def test_vertical_line(self):
        """Test ułożenia linii pionowej

        W przypadku ułożenia linii pionowej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        tpoles[1][0] = 1
        tpoles[2][0] = 1
        tpoles[3][0] = 1
        tpoles[4][0] = 1
        game_functions = GameFunctions(None, None, None, tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))

    def test_horizontal_line(self):
        """Test ułożenia linii poziomej

        W przypadku ułożenia linii poziomej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        tpoles[0][1] = 1
        tpoles[0][2] = 1
        tpoles[0][3] = 1
        tpoles[0][4] = 1

        # ważna jest tylko plansza
        game_functions = GameFunctions(None, None, None, tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))

    def test_oblique_line(self):
        """Test ułożenia linii skośnej

        W przypadku ułożenia linii skośnej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        tpoles[2][2] = 1
        tpoles[3][3] = 1
        tpoles[4][4] = 1
        tpoles[5][5] = 1

        # ważna jest tylko plansza
        game_functions = GameFunctions(None, None, None, tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))

    def test_longer_line(self):
        """Test ułożenia linii dłuższej niż 4

        W przypadku gdy linia jest dłuższa niż 4,
        wynik również powinien być pozytywny, czyli True"""

        tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        tpoles[0][0] = 1
        tpoles[0][1] = 1
        tpoles[0][2] = 1
        tpoles[0][3] = 1
        tpoles[0][4] = 1
        tpoles[0][5] = 1

        # ważna jest tylko plansza
        game_functions = GameFunctions(None, None, None, tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))


if __name__ == "__main":
    unittest.main()
