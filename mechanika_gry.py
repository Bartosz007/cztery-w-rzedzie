"""Plik przechowujący klasę odpowiadającą za mechanikę gry."""

from gracz_komputerowy import gracz_komputerowy

COLS = 7
ROWS = 6


class GameFunctions:
    """Klasę odpowiadająca za mechanikę gry."""
    def __init__(self, heigh, width, endgame, tpoles, tlevels, player, aiplayer, diff):
        """Konstruktor ładujący podstawowe zmienne."""
        self.__heigh = heigh
        self.__width = width
        self.hits = 0
        self.__end_game = endgame
        print("{}x{}".format(COLS, ROWS))

        self.__tpoles = tpoles
        self.__tlevels = tlevels
        self.__player = player
        self.__ai_player = aiplayer
        self.__diff = diff
        self.__canvas = None
        self.__f_stat = None

    def set_geometry(self, canvas, f_stat):
        """Metoda ładująca obiekt rysowniczy."""
        self.__canvas = canvas
        self.__f_stat = f_stat

    def draw(self):
        """Metoda rysującą każdą klatkę gry."""
        self.__canvas.delete("all")

        self.__canvas.create_rectangle(0, 0, self.__width, self.__heigh * 0.7, fill="#8A3500")

        rect_heigh = (self.__heigh * 0.60 / ROWS)
        rect_width = rect_heigh
        heigh_hole = (self.__heigh * 0.7 - (rect_heigh * 6)) / 7  # 7odstępów
        width_hole = (self.__width - (rect_heigh * 7)) / 8  # 8 odstępów

        for i in range(ROWS):
            for j in range(COLS):
                color = "white"
                if self.__tpoles[i][j] == -1:
                    color = "#FF2200"
                elif self.__tpoles[i][j] == 1:
                    color = "#FF9B21"

                self.__canvas.create_oval(width_hole * (1 + j) + rect_width * (1 + j),
                                          heigh_hole * (1 + i) + rect_heigh * (1 + i),
                                          width_hole * (1 + j) + rect_width * j,
                                          heigh_hole * (1 + i) + rect_heigh * i,
                                          fill=color, outline=color)

    def hit(self, col):
        """Metoda odpowiedziala za sposó liczenia w zależności od typu drugiego gracza."""
        if self.__ai_player:  # jeśli gramy z komputerem
            self.__aicalculate(col)
        else:
            self.__calculate(col)

    def change_player(self, player):
        """Metoda odzpowiedzialna za zmianę gracz po każdym strzale."""
        self.__player = player

        if self.__ai_player:
            if self.__player:
                self.set_stat("Zaczyna gracz numer 1")
            else:
                self.set_stat("Zaczyna gracz numer 2")

        else:
            self.set_stat("Zaczyna gracz numer 1")

        self.__ai_player = not self.__ai_player

    def change_diff(self, new_diff):
        """Metoda zmieniająca poziom trudności gracza komputerowego."""
        self.__diff = new_diff

    def set_stat(self, text):
        """Metoda odpowiedzialna za zmianę komunikatu."""
        self.__f_stat["text"] = text

    def __calculate(self, col):
        """Metoda odpoweidzialna za sprawdzanie wyników gry
        i kolejność dwóch graczy rzeczywsistych."""
        #  print(self.__tlevels)
        row = self.__tlevels[col]

        if row < 0:
            self.set_stat("Brak miejsca w tej kolumnie, strzel ponownie...")
            return

        status = False
        if self.__player:  # gracz nr 1
            self.__tpoles[row][col] = -1
            self.set_stat("Tura gracza 2")  # jeśli gramy z graczem drugim

            status = self.__check(row, col, -1)
            if status:
                # funckja z kończeniem gry
                self.set_stat("Wygrał gracz numer 1")

        else:
            self.__tpoles[row][col] = 1  # gracz nr 2

            self.set_stat("Tura gracza 1")
            status = self.__check(row, col, 1)
            if status:  # funckja z kończeniem gry
                self.set_stat("Wygrał gracz numer 2")

        self.draw()

        if status:
            print("wygra "+str(self.__player))
            if self.__player:
                self.__end_game(1)
            else:
                self.__end_game(2)

        self.hits = self.hits + 1
        if self.hits > 41:
            self.__end_game(4)

        self.__tlevels[col] = self.__tlevels[col] - 1
        self.__player = not self.__player

    def __aicalculate(self, col):
        """Metoda odpoweidzialna za sprawdzanie wyników gry
        i kolejność gracza rzeczywistego oraz komputerowego."""

        row = self.__tlevels[col]

        status = False
        if row < 0:
            self.set_stat("Brak miejsca w tej kolumnie, strzel ponownie...")
            return

        self.__tpoles[row][col] = -1

        status = self.__check(row, col, -1)
        if status:
            self.set_stat("Wygrał gracz numer 1")
            print("wygrał gracz 1")
            # funckja z kończeniem gry

        self.__tlevels[col] = self.__tlevels[col] - 1

        self.draw()

        if status:
            self.__end_game(1)
            return

        self.hits = self.hits + 1
        if self.hits > 41:
            self.set_stat("Remis")
            self.__end_game(4)
            return

        self.set_stat("Komputer myśli...")

        # ---------------sekcja komputera---------------------

        col2 = gracz_komputerowy(self.__tpoles, self.__tlevels, self.__diff)  # strzał komputera
        row2 = self.__tlevels[col2]
        # row2,col2 = ai(self.__tpoles,self.__tlevels,self.__rows,self.__cols)

        self.__tpoles[row2][col2] = 1

        status = self.__check(row2, col2, 1)
        if status:  # funckja z kończeniem gry
            self.set_stat("Wygrał komputer...")
            print("wygrał komputer")

        self.__tlevels[col2] = self.__tlevels[col2] - 1
        self.draw()

        if status:
            self.__end_game(3)
            print("komp wygrał")
            return

        self.hits = self.hits + 1
        if self.hits > 41:
            self.set_stat("Remis")
            self.__end_game(4)
            return

        self.set_stat("Tura gracza 1")

    def __check(self, row, col, sign):
        """Metoda sprawdzająca stan gry."""
        counter = 0
        for i in range(COLS):
            if self.__tpoles[row][i] == sign:
                counter = counter + 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(ROWS):
            if self.__tpoles[i][col] == sign:
                counter = counter + 1
                if counter == 4:
                    return True
            else:
                counter = 0

        # przekątna od lewej góra do prawej dół
        if col > row:
            eqal = row
        else:
            eqal = col
        brow = abs(eqal - row)
        bcol = abs(eqal - col)

        counter = 0
        while brow < 6 and bcol < 7:
            if self.__tpoles[brow][bcol] == sign:
                counter = counter + 1
                if counter == 4:
                    return True
            else:
                counter = 0
            brow = brow + 1
            bcol = bcol + 1

        # przekątna od prawej góra do lewej dół
        if (col + row) < 7:
            bcol = col + row
            brow = 0
        else:
            bcol = 6
            brow = row - (6 - col)
        counter = 0
        while brow < 6 and bcol >= 0:

            if self.__tpoles[brow][bcol] == sign:
                counter = counter + 1
                #     print(counter,brow,bcol)
                if counter == 4:
                    return True
            else:
                counter = 0

            brow = brow + 1
            bcol = bcol - 1

        return False
