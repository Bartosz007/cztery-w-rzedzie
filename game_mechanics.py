"""Plik przechowujący klasę odpowiadającą za mechanikę gry."""

from players import computer_player
from players import human_player
from utils.constants import Basic
from utils.constants import GameStatus
from utils.constants import Style

MAX_HITS = 41


class GameMechanics:
    """Klasę odpowiadająca za mechanikę gry."""

    def __init__(self, height, width, endgame, board, levels, players_array, canvas, stat):
        """Konstruktor ładujący podstawowe zmienne.

        Laduje zmienne używane w następnych metodach"""
        self.__height = height
        self.__width = width
        self.__end_game = endgame

        self.board = board
        self.levels = levels
        self.players_array = players_array

        self.current_player = 0  # musi ona występować, aby następowała zmienność tur
        self.hits = 0

        self.__canvas = canvas
        self.__stat = stat

    def draw(self):
        """Metoda rysującą każdą klatkę gry.

        Czyści całe okno gry a nastęnie rysuje wszystko od nowa."""
        self.__canvas.delete("all")

        self.__canvas.create_rectangle(0, 0, self.__width, self.__height * 0.7,
                                       fill=Style.CANVAS_BACKGROUND)

        rect_height = (self.__height * 0.60 / Basic.NUM_ROWS)
        rect_width = rect_height
        height_hole = (self.__height * 0.7 - (rect_height * Basic.NUM_ROWS)) / Basic.NUM_COLUMNS  # 7odstępów
        width_hole = (self.__width - (rect_height * Basic.NUM_COLUMNS)) / (Basic.NUM_COLUMNS + 1)  # 8 odstępów

        for i in range(Basic.NUM_ROWS):
            for j in range(Basic.NUM_COLUMNS):
                color = Style.DEFAULT_COIN_COLOR
                if self.board[i][j] == -Basic.COIN:
                    color = Style.PLAYER_ONE_COLOR
                elif self.board[i][j] == Basic.COIN:
                    color = Style.PLAYER_TWO_COLOR

                self.__canvas.create_oval(width_hole * (1 + j) + rect_width * (1 + j),
                                          height_hole * (1 + i) + rect_height * (1 + i),
                                          width_hole * (1 + j) + rect_width * j,
                                          height_hole * (1 + i) + rect_height * i,
                                          fill=color, outline=color)

    def hit(self, col=0):
        """Metoda odpowiedziala za wrzucanie monet

        Pilnuje kolejności graczy i sprawdza stan gry"""

        player = self.players_array[self.current_player]

        status = player.make_move(col, player.player_number)
        if status == GameStatus.WON:
            self.set_stat(player.end_info)
            self.__end_game(player.end_info)
            return GameStatus.WON
        elif status == GameStatus.COLUMN_NOT_FULL:
            if self.current_player:
                self.current_player = 0
            else:
                self.current_player = 1

            self.hits += 1

            try:
                self.draw()
            except AttributeError:
                print("Nie uzyskano elementu rysowniczego")

            if self.hits > MAX_HITS:
                self.__end_game("Remis!")
                self.set_stat("Remis!")
                return GameStatus.DRAW

            self.set_stat(self.players_array[self.current_player].turn_info)
            if self.players_array[self.current_player].type_of_player == Basic.COMPUTER:
                self.hit()

        else:
            self.set_stat("Brak miejsca w tej kolumnie, strzel ponownie...")

        return GameStatus.STILL_IN_GAME

    def change_player(self, difficulty=0):
        """Metoda odzpowiedzialna za zmianę gracza po każdym strzale."""

        if self.players_array[1].type_of_player == Basic.COMPUTER:
            self.players_array[1] = human_player.HumanPlayer(self.board, self.levels,
                                                             Basic.PLAYER_TWO)
        else:
            self.players_array[1] = computer_player.ComputerPlayer(self.board, self.levels,
                                                                   difficulty)

        self.current_player = 0
        self.set_stat(self.players_array[self.current_player].begin_info)

    def change_difficulty(self, txt):
        """Metoda zmieniająca poziom trudności gracza komputerowego."""

        difficulties = ["Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber"]
        index = difficulties.index(txt)

        if self.players_array[1].type_of_player == Basic.COMPUTER:
            self.players_array[1].change_difficulty(index)

    def set_stat(self, text):
        """Metoda odpowiedzialna za zmianę komunikatu."""
        try:
            self.__stat["text"] = text
        except TypeError:
            print("Nie udało się uzyskać bloku text")
