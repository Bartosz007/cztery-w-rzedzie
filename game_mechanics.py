"""Plik przechowujący klasę odpowiadającą za mechanikę gry."""

import players.computer_player as cp
import players.human_player as hp

from utils.constans import GameStatus, Basic

MAX_HITS = 41


class GameMechanics:
    """Klasę odpowiadająca za mechanikę gry."""

    def __init__(self, heigh, width, endgame, board, levels, first_player, second_player):
        """Konstruktor ładujący podstawowe zmienne.

        Laduje zmienne używane w następnych metodach"""
        self.__heigh = heigh
        self.__width = width
        self.__end_game = endgame

        self.board = board
        self.levels = levels
        self.first_player = first_player
        self.second_player = second_player

        self.round = True  # musi ona występować, aby następowała zmienność tur
        self.hits = 0

        self.__canvas = None
        self.__stat = None

    def set_geometry(self, canvas, stat):
        """Metoda ładująca obiekt rysowniczy."""
        self.__canvas = canvas
        self.__stat = stat

    def draw(self):
        """Metoda rysującą każdą klatkę gry.

        Czyści całe okno gry a nastęnie rysuje wszystko od nowa."""
        self.__canvas.delete("all")

        self.__canvas.create_rectangle(0, 0, self.__width, self.__heigh * 0.7, fill="#8A3500")

        rect_heigh = (self.__heigh * 0.60 / Basic.ROWS)
        rect_width = rect_heigh
        heigh_hole = (self.__heigh * 0.7 - (rect_heigh * Basic.ROWS)) / 7  # 7odstępów
        width_hole = (self.__width - (rect_heigh * Basic.COLS)) / 8  # 8 odstępów

        for i in range(Basic.ROWS):
            for j in range(Basic.COLS):
                color = "white"
                if self.board[i][j] == -Basic.COIN:
                    color = "#FF2200"
                elif self.board[i][j] == Basic.COIN:
                    color = "#FF9B21"

                self.__canvas.create_oval(width_hole * (1 + j) + rect_width * (1 + j),
                                          heigh_hole * (1 + i) + rect_heigh * (1 + i),
                                          width_hole * (1 + j) + rect_width * j,
                                          heigh_hole * (1 + i) + rect_heigh * i,
                                          fill=color, outline=color)

    def hit(self, col=0):
        """Metoda odpowiedziala za wrzucanie monet

        Pilnuje kolejności graczy i sprawdza stan gry"""

        if self.round:

            status = self.first_player.make_move(col, 1)
            if status == GameStatus.WON:
                self.set_stat("Wygrał gracz numer 1")
                self.__end_game(GameStatus.PLAYER_ONE_WON)
                return GameStatus.PLAYER_ONE_WON
            elif status == GameStatus.COLUMN_NOT_FULL:
                self.round = not self.round
                self.hits += 1

                try:
                    self.draw()
                except:
                    print("Nie uzyskano elementu rysowniczego")

                if self.hits > MAX_HITS:
                    self.__end_game(GameStatus.DRAW)
                    self.set_stat("Remis!")
                    return GameStatus.DRAW

                if isinstance(self.second_player, cp.ComputerPlayer):
                    self.set_stat("Tura komputera")
                    self.hit()  # sztuczne wywołanie akcji komputera
                else:
                    self.set_stat("Tura drugiego gracza")
            else:
                self.set_stat("Podana kolumna jest zajęta")

            # make_move może też zwrócić COLUMN_FULL, czyli gracz musi strzelić jeszcze raz

        else:
            status = self.second_player.make_move(col, -1)
            if status == GameStatus.WON:
                if isinstance(self.second_player, cp.ComputerPlayer):
                    self.set_stat("Wygrał komputer")
                    self.__end_game(GameStatus.COMPUTER_WON)
                    return GameStatus.COMPUTER_WON
                else:
                    self.set_stat("Wygrał gracz numer 2")
                    self.__end_game(GameStatus.PLAYER_TWO_WON)
                    return GameStatus.PLAYER_ONE_WON

            elif status == GameStatus.COLUMN_NOT_FULL:
                self.round = not self.round
                self.hits += 1
                self.set_stat("Tura pierwszego gracza")

                try:
                    self.draw()
                except:
                    print("Nie uzyskano elementu rysowniczego")

                if self.hits > MAX_HITS:
                    self.__end_game(GameStatus.DRAW)
                    self.set_stat("Remis!")
                    return GameStatus.DRAW
            else:
                self.set_stat("Podana kolumna jest zajęta")

        return GameStatus.STILL_IN_GAME

    def change_player(self, difficulty=0):
        """Metoda odzpowiedzialna za zmianę gracza po każdym strzale."""
        if isinstance(self.second_player, cp.ComputerPlayer):
            if self.round:
                self.set_stat("Zaczyna gracz numer 1")
            else:
                self.set_stat("Zaczyna gracz numer 2")

            self.second_player = hp.HumanPlayer(self.board, self.levels)
        else:
            self.round = True
            self.set_stat("Zaczyna gracz numer 1")
            self.second_player = cp.ComputerPlayer(self.board, self.levels, difficulty)

    def change_diff(self, txt):
        """Metoda zmieniająca poziom trudności gracza komputerowego."""

        diffs = ["Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber"]
        index = diffs.index(txt)

        if isinstance(self.second_player, cp.ComputerPlayer):
            self.second_player.change_difficulty(index)

    def set_stat(self, text):
        """Metoda odpowiedzialna za zmianę komunikatu."""
        try:
            self.__stat["text"] = text
        except TypeError:
            print("Nie udało się uzyskać bloku text")
