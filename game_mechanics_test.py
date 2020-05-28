"""Plik z klasą testującą metody gry z klasy GameFunctions"""

import unittest

import utils.players_utils as pu
import players.human_player as hp
import game_mechanics as gm

from utils.constans import Basic


class TestGameMechanics(unittest.TestCase):
    """Klasa zawierająca testy programu"""

    def setUp(self):
        self.board = [[0 for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        self.levels = [5 for col in range(Basic.COLS)]

    def test_vertical_line(self):
        """Test ułożenia linii pionowej

        W przypadku ułożenia linii pionowej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        self.board[1][0] = 1
        self.board[2][0] = 1
        self.board[3][0] = 1
        self.board[4][0] = 1

        # ważna jest tylko plansza
        game_functions = gm.GameMechanics(None, None, None, self.board, None, None, None)
        self.assertTrue(pu.check(self.board, 0, 0, 1))

    def test_horizontal_line(self):
        """Test ułożenia linii poziomej

        W przypadku ułożenia linii poziomej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        self.board = [[0 for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        self.board[0][1] = 1
        self.board[0][2] = 1
        self.board[0][3] = 1
        self.board[0][4] = 1

        game_functions = gm.GameMechanics(None, None, None, self.board, None, None, None)
        self.assertTrue(pu.check(self.board, 0, 0, 1))

    def test_oblique_line(self):
        """Test ułożenia linii skośnej

        W przypadku ułożenia linii skośnej,
        funkcja powinna dać znak o wygranej jednego gracza, zwracając True"""

        self.board = [[0 for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        self.board[2][2] = 1
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[5][5] = 1

        game_functions = gm.GameMechanics(None, None, None, self.board, None, None, None)
        self.assertTrue(pu.check(self.board, 0, 0, 1))

    def test_longer_line(self):
        """Test ułożenia linii dłuższej niż 4

        W przypadku gdy linia jest dłuższa niż 4,
        wynik również powinien być pozytywny, czyli True"""

        self.board = [[0 for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        self.board[0][0] = 1
        self.board[0][1] = 1
        self.board[0][2] = 1
        self.board[0][3] = 1
        self.board[0][4] = 1
        self.board[0][5] = 1

        game_functions = gm.GameMechanics(None, None, None, self.board, None, None, None)
        self.assertTrue(pu.check(self.board, 0, 0, 1))

    def test_two_shots(self):
        """Test wykonujący po dwa strzały każdym kolorem monety

        Powinny zostać wrzucone i spać na dół pola gry,
        lub zatrzymać się na już wrzuconej monecie"""

        compare_table = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0, 0], [0, 1, -1, 0, 0, 1, 0]]

        first_player = hp.HumanPlayer(self.board, self.levels)
        second_player = hp.HumanPlayer(self.board, self.levels)

        game_functions = gm.GameMechanics(None, None, None,
                                          self.board, self.levels, first_player, second_player)

        game_functions.hit(1)
        game_functions.hit(2)
        game_functions.hit(1)
        game_functions.hit(2)
        game_functions.hit(5)

        self.assertEqual(self.board, compare_table)


if __name__ == "__main__":
    unittest.main()
