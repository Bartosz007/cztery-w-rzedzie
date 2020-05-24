"""Plik zaiwerający klasę, obsługującą gracza komputerowego."""
from random import randint

COLS = 7
ROWS = 6
INF = 999999999


class GraczKomputerowy:
    """Klasa obsługująca gracza komputerowego."""

    def __init__(self, tpoles, tlevels, diff):
        """Konstruktor przyjmujący podstawowe dane do późnijeszych obliczeń."""
        self.__ctpoles = [[tpoles[row][col] for col in range(COLS)] for row in range(ROWS)]
        self.__ctlevels = [tlevels[x] for x in range(COLS)]
        self.__diff = diff

    def make_move(self):
        """Metoda zwracająca kolumnę strzału.

        W zależności od poziomu trudności zwraca pole wylosowane lub
        obliczone za pomocą algorytmu optymalizującego minimax."""
        fields = self.right_fields(self.__ctlevels)
        col = 0
        if self.__diff == 0:
            col = self.random_field(fields)
        else:
            col = self.minimax(self.__ctpoles, self.__ctlevels, self.__diff, True)[0]

        return col

    @staticmethod
    def right_fields(tlevels):
        """Metoda statyczna zwracająca możliwe pola strzału."""
        tab = []
        for i, value in enumerate(tlevels):
            if value >= 0:
                tab.append((value, i))

        return tab

    @staticmethod
    def random_field(fields):
        """Metoda statyczna losująca pole strzału."""

        rand = randint(0, len(fields) - 1)
        return fields[rand][1]

    def minimax(self, tpoles, tlevels, depth, maximazing):
        """Metoda wybierająca najoptymalniejsze pole strzału algorytmem minimax."""

        fields = self.right_fields(tlevels)
        if depth == 0 or len(fields) == 0:
            return None, self.score_board(tpoles)
        if maximazing:
            value = -INF
            column = 1
            for row, col in fields:
                ctpoles = [[tpoles[r][c] for c in range(COLS)] for r in range(ROWS)]
                ctlevels = [tlevels[x] for x in range(COLS)]

                ctpoles[row][col] = 1
                ctlevels[col] = ctlevels[col] - 1

                score = self.minimax(ctpoles, ctlevels, depth - 1, False)[1]
                if score > value:
                    value = score
                    column = col

            return column, value
        else:
            value = INF
            column = 1
            for row, col in fields:
                ctpoles = [[tpoles[r][c] for c in range(COLS)] for r in range(ROWS)]
                ctlevels = [tlevels[x] for x in range(COLS)]

                ctpoles[row][col] = -1
                ctlevels[col] = ctlevels[col] - 1

                score = self.minimax(ctpoles, ctlevels, depth - 1, True)[1]
                if score < value:
                    value = score
                    column = col

            return column, value

    @staticmethod
    def score_board(tpoles):
        """Metoda oceniająca aktualny stan planszy.

        Metoda analizuje aktualny stan planszy i zwraca ocenę."""
        pos = [0 for i in range(9)]

        for i in range(ROWS):
            score = 0
            for j in range(3):
                score = score + tpoles[i][j]

            for j in range(3, COLS):
                score = score + tpoles[i][j]
                pos[score + 4] = pos[score + 4] + 1

                score = score - tpoles[i][j - 3]

        for i in range(COLS):
            score = 0
            for j in range(3):
                score = score + tpoles[j][i]

            for j in range(3, ROWS):
                score = score + tpoles[j][i]
                pos[score + 4] = pos[score + 4] + 1

                score = score - tpoles[j - 3][i]

        for i in range(ROWS - 3):
            for j in range(COLS - 3):
                score = 0

                for shift in range(4):
                    row = i + shift
                    col = j + shift
                    score = score - score + tpoles[row][col]

                pos[score + 4] = pos[score + 4] + 1

        for i in range(3, ROWS):
            for j in range(COLS - 3):
                score = 0

                for shift in range(4):
                    row = i - shift
                    col = j + shift
                    score = score + tpoles[row][col]

                pos[score + 4] = pos[score + 4] + 1

        player = 0 * pos[0] + 5 * pos[1] + 2 * pos[2] + pos[3]
        computer = pos[5] + 2 * pos[6] + 5 * pos[7] + 0 * pos[8]
        # ogromne znaczenie mają pozycje pos[1] i pos[6]

        if pos[0] != 0:
            return -3333333333333333333
        elif pos[8] != 0:
            return 5555555555555555554
        else:
            return computer - player
