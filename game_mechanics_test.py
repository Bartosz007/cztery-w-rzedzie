"""Plik z klasą testującą metody gry z klasy GameFunctions"""

import unittest

import constans
from game_mechanics import GameMechanics
from game_frame import GameFrame


class TestGameMechanics(unittest.TestCase):
    """Klasa testująca metody z klasy GameMechanics"""

    def setUp(self):
        self.tpoles = [[0 for col in range(constans.COLS)] for row in range(constans.ROWS)]
        self.tlevels = [5 for col in range(constans.COLS)]


    def test_two_shots(self):
        """Test wykonujący po dwa strzały każdym kolorem monety

        Powinny zostać wrzucone i spać na dół pola gry,
        lub zatrzymać się na już wrzuconej monecie"""

        compare_table = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0, 0]]

        game_functions = GameMechanics(None, None, GameFrame.end_game,
                                       self.tpoles, self.tlevels, False, None, None)
        game_functions.calculate(1)
        game_functions.calculate(2)
        game_functions.calculate(1)
        game_functions.calculate(2)
        game_functions.calculate(1)
        self.assertEqual(self.tpoles, compare_table)



    def test_vertical_line(self):
        """Test ułożenia linii pionowej

        W przypadku ułożenia linii pionowej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        self.tpoles[1][0] = 1
        self.tpoles[2][0] = 1
        self.tpoles[3][0] = 1
        self.tpoles[4][0] = 1
        game_functions = GameMechanics(None, None, None, self.tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))

    def test_horizontal_line(self):
        """Test ułożenia linii poziomej

        W przypadku ułożenia linii poziomej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        self.tpoles = [[0 for col in range(constans.COLS)] for row in range(constans.ROWS)]
        self.tpoles[0][1] = 1
        self.tpoles[0][2] = 1
        self.tpoles[0][3] = 1
        self.tpoles[0][4] = 1

        # ważna jest tylko plansza
        game_functions = GameMechanics(None, None, None, self.tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))

    def test_oblique_line(self):
        """Test ułożenia linii skośnej

        W przypadku ułożenia linii skośnej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        self.tpoles = [[0 for col in range(constans.COLS)] for row in range(constans.ROWS)]
        self.tpoles[2][2] = 1
        self.tpoles[3][3] = 1
        self.tpoles[4][4] = 1
        self.tpoles[5][5] = 1

        # ważna jest tylko plansza
        game_functions = GameMechanics(None, None, None, self.tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))

    def test_longer_line(self):
        """Test ułożenia linii dłuższej niż 4

        W przypadku gdy linia jest dłuższa niż 4,
        wynik również powinien być pozytywny, czyli True"""

        self.tpoles = [[0 for col in range(constans.COLS)] for row in range(constans.ROWS)]
        self.tpoles[0][0] = 1
        self.tpoles[0][1] = 1
        self.tpoles[0][2] = 1
        self.tpoles[0][3] = 1
        self.tpoles[0][4] = 1
        self.tpoles[0][5] = 1

        # ważna jest tylko plansza
        game_functions = GameMechanics(None, None, None, self.tpoles, None, None, None, None)
        self.assertTrue(game_functions.check(0, 0, 1))


if __name__ == "__main__":
    unittest.main()
