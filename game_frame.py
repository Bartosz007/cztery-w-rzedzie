"""Plik przechowujący klasę odpowiadający za odpowiednią budowę okna gry oraz jego elementów."""

import functools
import tkinter as tk
from tkinter import messagebox

import game_mechanics
import players
from utils import players_utils
from utils.constants import Basic
from utils.constants import Style


GLOBAL_SCALE = 1
WINDOW_SCALE_W = GLOBAL_SCALE * 0.6
WINDOW_SCALE_H = GLOBAL_SCALE * 0.85


class GameFrame:
    """Klasa odpowiadająca za odpowiednią budowę okna gry oraz jego elementów."""

    def __init__(self, window):
        """Konstruktor budujący okno gry.

         Buduje okno o odpowiednim rozmiarze oraz tworzący zmienne
        i tablice przechowujące podstawowe dane o grze."""

        screen_height = window.winfo_screenheight()  # rozdzielczość ekranu
        screen_width = window.winfo_screenwidth()

        self.__window = window
        self.__window_height = int(screen_height * WINDOW_SCALE_H)
        self.__window_width = int(screen_width * WINDOW_SCALE_W)
        self.__window.geometry("{}x{}+{}+{}".format(
            int(self.__window_width),
            int(self.__window_height),
            int(self.__window_width * 0.3),
            int(self.__window_height * 0.08)))  # rozmiar okna i pozycja po uruchomeniu

        self.__ai_player = True
        self.__stat = None
        self.__canvas = None
        self.__rbt_computer = None
        self.__rbt_player = None
        self.__s_difficulty = None
        self.load_geometry()

        board, levels = players_utils.start_data()
        difficulty = 0

        first_player = players.human_player.HumanPlayer(board, levels, Basic.PLAYER_ONE)
        second_player = players.computer_player.ComputerPlayer(board, levels,
                                                               Basic.PLAYER_TWO, difficulty)
        players_array = [first_player, second_player]

        self.__game = game_mechanics.GameMechanics(self.__window_height, self.__window_width,
                                                   self.end_game, board, levels, players_array,
                                                   self.__canvas, self.__stat)

    def load_geometry(self):
        """Metoda tworząca wszystkie elementy okna gry."""
        # bloki główne
        f_stat_menu = tk.Frame(self.__window, width=self.__window_width,
                               height=self.__window_height * 0.08, bg=Style.BACKGROUND_COLOR)
        f_stat_menu.pack_propagate(0)
        f_stat_menu.pack()

        f_top_menu = tk.Frame(self.__window, width=self.__window_width,
                              height=self.__window_height * 0.07, bg=Style.BACKGROUND_COLOR)
        f_top_menu.pack_propagate(0)
        f_top_menu.pack()
        f_top_in_menu = tk.Frame(f_top_menu, width=self.__window_width * 0.95,
                                 height=self.__window_height * 0.07, bg=Style.BACKGROUND_COLOR)
        f_top_in_menu.pack_propagate(0)
        f_top_in_menu.pack()  # ten blok istnieje, aby nie pojawiały się białe paski z boku

        f_board = tk.Frame(self.__window, width=self.__window_width,
                           height=self.__window_height * 0.7, bg=Style.BACKGROUND_COLOR)
        f_board.pack_propagate(0)
        f_board.pack()

        # bloki menu dolneg =-----------------------------------------------
        f_bottom_menu = tk.Frame(self.__window, width=self.__window_width,
                                 height=self.__window_height * 0.15, bg=Style.BACKGROUND_COLOR)
        f_bottom_menu.pack_propagate(0)
        f_bottom_menu.pack()

        f_bottom_left = tk.Frame(f_bottom_menu, width=self.__window_width * (2 / 3),
                                 height=self.__window_height * 0.2, bg=Style.BACKGROUND_COLOR)
        f_bottom_left.pack_propagate(0)
        f_bottom_left.pack(side=tk.LEFT)

        f_bottom_right = tk.Frame(f_bottom_menu, width=self.__window_width / 3,
                                  height=self.__window_height * 0.2, bg=Style.BACKGROUND_COLOR)
        f_bottom_right.pack_propagate(0)
        f_bottom_right.pack(side=tk.RIGHT)

        f_player_menu = tk.Frame(f_bottom_left, width=self.__window_width * (2 / 3),
                                 height=self.__window_height * 0.1, bg=Style.BACKGROUND_COLOR)
        f_player_menu.pack()

        f_difficulty_menu = tk.Frame(f_bottom_left, width=self.__window_width * (2 / 3),
                                     height=self.__window_height * 0.1, bg=Style.BACKGROUND_COLOR)
        f_difficulty_menu.pack_propagate(0)
        f_difficulty_menu.pack()

        f_reset_menu = tk.Frame(f_bottom_right, width=self.__window_width / 3,
                                height=self.__window_height * 0.2, bg=Style.BACKGROUND_COLOR)
        f_reset_menu.pack_propagate(0)
        f_reset_menu.pack()

        # panel komunikatów=----------------------------------------------------------
        self.__stat = tk.Label(f_stat_menu, bg=Style.BACKGROUND_COLOR, text="komunikat",
                               font=(Style.FONT, Style.FONT_SIZE * 2))
        self.__stat.pack(side=tk.TOP)

        # panel przycisków
        fixed_window_width = self.__window_width * 0.95 / Basic.NUM_COLUMNS
        for index in range(Basic.NUM_COLUMNS):
            frame = tk.Frame(f_top_in_menu, width=fixed_window_width,
                             height=self.__window_height * 0.1, bg=Style.BACKGROUND_COLOR)
            frame.pack_propagate(0)
            frame.pack(side=tk.LEFT)
            button = tk.Button(frame, text="{}".format(index + 1), padx=self.__window_width / 28,
                               pady=self.__window_height / 80, bg=Style.BUTTON_COLOR)
            button.config(command=functools.partial(self.__hit, index))
            button.pack(side=tk.BOTTOM)

        # panel środkowy
        self.__canvas = tk.Canvas(f_board, width=self.__window_width,
                                  height=self.__window_height * 0.7)
        self.__canvas.pack()

        # panel Player Menu=-----------------------------------------------------------------
        l_pm = tk.Label(f_player_menu, text="Ustawienia drugiego gracza: ",
                        font=(Style.FONT, Style.FONT_SIZE - 1), bg=Style.BACKGROUND_COLOR)
        l_pm.pack(side=tk.TOP)

        grup = True
        self.__rbt_computer = tk.Radiobutton(f_player_menu, text="Komputer", variable=grup, value=1,
                                             font=(Style.FONT, Style.FONT_SIZE - 2), indicatoron=0,
                                             bg=Style.BUTTON_COLOR,
                                             command=lambda: self.change_player(True),
                                             padx=25, pady=2)
        self.__rbt_computer.pack(side=tk.LEFT)

        self.__rbt_player = tk.Radiobutton(f_player_menu, text="Człowiek", variable=grup, value=2,
                                           font=(Style.FONT, Style.FONT_SIZE - 2), indicatoron=0,
                                           bg=Style.BUTTON_COLOR,
                                           command=lambda: self.change_player(False),
                                           padx=25, pady=2)
        self.__rbt_player.pack(side=tk.RIGHT)

        if self.__ai_player:
            self.__rbt_computer.select()
        else:
            self.__rbt_player.select()

        l_dm = tk.Label(f_difficulty_menu, width=int(self.__window_width / 20),
                        bg=Style.BACKGROUND_COLOR, text="Poziom trudności: ",
                        font=(Style.FONT, Style.FONT_SIZE - 1))
        l_dm.pack(side=tk.TOP)
        levels = ("Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber")
        self.__s_difficulty = tk.Spinbox(f_difficulty_menu, width=int(self.__window_width / 25),
                                         bg=Style.BACKGROUND_COLOR,
                                         justify=tk.CENTER, values=levels,
                                         font=(Style.FONT, Style.FONT_SIZE), state="readonly")
        self.__s_difficulty.config(command=self.change_difficulty)
        self.__s_difficulty.pack(side=tk.BOTTOM)

        # panel Reset
        bt_reset = tk.Button(f_reset_menu, text="Reset", padx=int(self.__window_width / 30),
                             pady=self.__window_height, font=(Style.FONT, Style.FONT_SIZE + 5),
                             bg=Style.BUTTON_COLOR)
        bt_reset.config(command=self.__reset_game)
        bt_reset.pack()

        self.__stat["text"] = "Zaczyna gracz numer 1"

    def start_game(self):
        """Metoda uruchamiająca główną pętle gry."""
        print("otworzono okno gry...")

        self.__game.draw()

        self.__window.mainloop()
        print("zamknięto okno gry")

    def change_player(self, player):
        """Metoda reagująca na przyckiski odpowiedzialne za zmianę gracza."""

        if self.__ai_player != player:
            self.__ai_player = player

            if not self.__ai_player:
                self.__s_difficulty.config(state=tk.DISABLED)
            else:
                self.__s_difficulty.config(state="readonly")
                self.__game.change_difficulty(self.__s_difficulty.get())

            self.__game.change_player()

    def change_difficulty(self):
        """Metoda reagująca na spinboxa odpowiedzialnego
        za zmianę poziomu umiejętności dla gracza komputerowego."""

        self.__game.change_difficulty(self.__s_difficulty.get())

    def end_game(self, info):
        """Metoda odpowiedzialna za wyświetlanie dodatkowego okna i kończenie gry."""

        message = tk.messagebox.askquestion(title="Connect4",
                                            message="{} czy chcesz kontynuować?".format(info))

        if message == "yes":
            self.__reset_game()
        else:
            self.__window.destroy()

    def __reset_game(self):
        """Metoda odpowiedzialna za resetowanie stanu gry.

        Resetuje ona ustawienia gry oraz planszy,
        dzięki czemu zamykanie okna nie jest wymagane."""

        old_second_player = self.__game.players_array[1].type_of_player
        del self.__game
        print("zresetowano grę....")
        print()

        board, levels = players_utils.start_data()

        first_player = players.human_player.HumanPlayer(board, levels, Basic.PLAYER_ONE)

        if old_second_player == Basic.COMPUTER:
            difficulties = ["Losowy", "Łatwy", "Też łatwy",
                            "Średni", "Trudny", "Bardzo trudny", "Uber"]
            index = difficulties.index(self.__s_difficulty.get())
            new_second_player = players.computer_player.ComputerPlayer(board, levels,
                                                                       Basic.PLAYER_TWO, index)
        else:
            new_second_player = players.human_player.HumanPlayer(board, levels, Basic.PLAYER_TWO)

        players_array = [first_player, new_second_player]
        self.__game = game_mechanics.GameMechanics(self.__window_height, self.__window_width,
                                                   self.end_game, board, levels, players_array,
                                                   self.__canvas, self.__stat)

        print("władowano dane gry...")

        # funkcje geometrii
        self.__rbt_computer["state"] = tk.ACTIVE
        self.__rbt_player["state"] = tk.ACTIVE
        self.__s_difficulty["state"] = "readonly"

        if new_second_player:
            self.__rbt_computer.select()
        else:
            self.__rbt_player.select()

        # ustawienie początkowego komunikatu
        self.__game.set_stat("Zaczyna gracz numer 1")

        print("władowano geometrie...")

        print("przeładowano okno gry...")
        self.__game.draw()

    def __hit(self, index):
        """Metoda reagująca na przyciski od wyboru kolumny."""
        self.__rbt_computer["state"] = tk.DISABLED
        self.__rbt_player["state"] = tk.DISABLED
        self.__s_difficulty["state"] = tk.DISABLED
        self.__game.hit(index)
