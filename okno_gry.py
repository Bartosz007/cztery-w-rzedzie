"""Plik przechowujący klasę odpowiadający za odpowiednią budowę okna gry oraz jego elementów."""

import tkinter as tk

from functools import partial
from random import choice
from tkinter import messagebox

from mechanika_gry import GameFunctions

COLS = 7
ROWS = 6
GLOBAL_SCALE = 1
WINDOW_SCALE_W = GLOBAL_SCALE * 0.6
WINDOW_SCALE_H = GLOBAL_SCALE * 0.85
FONT = "Times New Roman"
FONT_SIZE = 15
COLOR = "#296380"
SECOND_COLOR = "#D15304"

class ConnectFour:
    """Klasa odpowiadająca za odpowiednią budowę okna gry oraz jego elementów."""

    def __init__(self, window):
        """Konstruktor budujący okno gry.

         Buduje okno o odpowiednim rozmiarze oraz tworzący zmienne
        i tablice przechowujące podstawowe dane o grze."""

        screen_heigh = window.winfo_screenheight()  # rozdzielczość ekranu
        screen_width = window.winfo_screenwidth()

        self.__window = window
        self.__window_heigh = int(screen_heigh * WINDOW_SCALE_H)
        self.__window_width = int(screen_width * WINDOW_SCALE_W)
        self.__window.geometry("{}x{}+{}+{}".format(
            int(self.__window_width),
            int(self.__window_heigh),
            int(self.__window_width * 0.3),
            int(self.__window_heigh * 0.08)))  # rozmiar okna i pozycja po uruchomeniu

        print("skonfigurowano okno gry...")

        # tablica z każdym polem
        self.__tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        # tablica przechowująca poziomy każdej kolumny
        self.__tlevels = [5 for col in range(COLS)]
        self.__player = choice([True, False])

        # czy gracz komputerowy jest włączony True - włączony, False - wyłączony
        self.__ai_player = True
        # poziom trudnosci sztucznej inteligencji 0-7
        self.__diff = 0
        self.__game = GameFunctions(self.__window_heigh, self.__window_width,
                                    self.end_game, self.__tpoles, self.__tlevels,
                                    self.__player, self.__ai_player, self.__diff)
        # warunek, że jeśli gramy z komputerem, to zawsze gracz zaczyna
        if self.__ai_player:
            self.__player = True

        print("władowano dane gry...")

        self.__l_stat = None
        self.__canvas = None
        self.__rbt_computer = None
        self.__rbt_player = None
        self.__s_diff = None

    def load_geometry(self):
        """Metoda tworząca wszystkie elementy okna gry."""
        # bloki główne
        f_stat_menu = tk.Frame(self.__window, width=self.__window_width,
                               heigh=self.__window_heigh * 0.08, bg=COLOR)
        f_stat_menu.pack_propagate(0)
        f_stat_menu.pack()

        f_top_menu = tk.Frame(self.__window, width=self.__window_width,
                              heigh=self.__window_heigh * 0.07, bg=COLOR)
        f_top_menu.pack_propagate(0)
        f_top_menu.pack()
        f_top_in_menu = tk.Frame(f_top_menu, width=self.__window_width * 0.95,
                                 heigh=self.__window_heigh * 0.07, bg=COLOR)
        f_top_in_menu.pack_propagate(0)
        f_top_in_menu.pack()  # ten blok istnieje, aby nie pojawiały się białe paski z boku

        f_board = tk.Frame(self.__window, width=self.__window_width,
                           heigh=self.__window_heigh * 0.7, bg=COLOR)
        f_board.pack_propagate(0)
        f_board.pack()

        # bloki menu dolneg =-----------------------------------------------
        f_bottom_menu = tk.Frame(self.__window, width=self.__window_width,
                                 heigh=self.__window_heigh * 0.15, bg=COLOR)
        f_bottom_menu.pack_propagate(0)
        f_bottom_menu.pack()

        f_bottom_left = tk.Frame(f_bottom_menu, width=self.__window_width * (2 / 3),
                                 heigh=self.__window_heigh * 0.2, bg=COLOR)
        f_bottom_left.pack_propagate(0)
        f_bottom_left.pack(side=tk.LEFT)

        f_bottom_right = tk.Frame(f_bottom_menu, width=self.__window_width / 3,
                                  heigh=self.__window_heigh * 0.2, bg=COLOR)
        f_bottom_right.pack_propagate(0)
        f_bottom_right.pack(side=tk.RIGHT)

        f_player_menu = tk.Frame(f_bottom_left, width=self.__window_width * (2 / 3),
                                 heigh=self.__window_heigh * 0.1, bg=COLOR)
        f_player_menu.pack()

        f_diff_menu = tk.Frame(f_bottom_left, width=self.__window_width * (2 / 3),
                               heigh=self.__window_heigh * 0.1, bg=COLOR)
        f_diff_menu.pack_propagate(0)
        f_diff_menu.pack()

        f_reset_menu = tk.Frame(f_bottom_right, width=self.__window_width / 3,
                                heigh=self.__window_heigh * 0.2, bg=COLOR)
        f_reset_menu.pack_propagate(0)
        f_reset_menu.pack()

        # panel komunikatów=----------------------------------------------------------
        self.__l_stat = tk.Label(f_stat_menu, bg=COLOR, text="komunikat",
                                 font=(FONT, FONT_SIZE * 2))
        self.__l_stat.pack(side=tk.TOP)

        # panel przycisków
        fixed_window_width = self.__window_width * 0.95 / 7
        for index in range(COLS):
            frame = tk.Frame(f_top_in_menu, width=fixed_window_width,
                             heigh=self.__window_heigh * 0.1, bg=COLOR)
            frame.pack_propagate(0)
            frame.pack(side=tk.LEFT)
            button = tk.Button(frame, text="{}".format(index + 1), padx=self.__window_width / 28,
                               pady=self.__window_heigh / 80, bg=SECOND_COLOR)
            button.config(command=partial(self.__bt_hit, index))
            button.pack(side=tk.BOTTOM)

        # panel środkowy
        self.__canvas = tk.Canvas(f_board, width=self.__window_width,
                                  height=self.__window_heigh * 0.7)
        self.__canvas.pack()

        # panel Player Menu=-----------------------------------------------------------------
        l_pm = tk.Label(f_player_menu, text="Ustawienia drugiego gracza: ",
                        font=(FONT, FONT_SIZE - 1), bg=COLOR)
        l_pm.pack(side=tk.TOP)

        grup = True
        self.__rbt_computer = tk.Radiobutton(f_player_menu, text="Komputer", variable=grup, value=1,
                                             font=(FONT, FONT_SIZE - 2), indicatoron=0,
                                             bg=SECOND_COLOR,
                                             command=lambda: self.change_player(True),
                                             padx=25, pady=2)
        self.__rbt_computer.pack(side=tk.LEFT)

        self.__rbt_player = tk.Radiobutton(f_player_menu, text="Człowiek", variable=grup, value=2,
                                           font=(FONT, FONT_SIZE - 2), indicatoron=0,
                                           bg=SECOND_COLOR,
                                           command=lambda: self.change_player(False),
                                           padx=25, pady=2)
        self.__rbt_player.pack(side=tk.RIGHT)

        if self.__ai_player:
            self.__rbt_computer.select()
        else:
            self.__rbt_player.select()

        # panel Diff Menu=------------------------------------------------
        l_dm = tk.Label(f_diff_menu, width=int(self.__window_width / 20), bg=COLOR,
                        text="Poziom trudności: ", font=(FONT, FONT_SIZE - 1))
        l_dm.pack(side=tk.TOP)
        levels = ("Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber")
        self.__s_diff = tk.Spinbox(f_diff_menu, width=int(self.__window_width / 25), bg=COLOR,
                                   justify=tk.CENTER, values=levels,
                                   font=(FONT, FONT_SIZE), state="readonly")
        self.__s_diff.config(command=self.change_level)
        self.__s_diff.pack(side=tk.BOTTOM)

        # panel Reset
        bt_reset = tk.Button(f_reset_menu, text="Reset", padx=int(self.__window_width / 30),
                             pady=self.__window_heigh, font=(FONT, FONT_SIZE + 5), bg=SECOND_COLOR)
        bt_reset.config(command=self.__reset_game)
        bt_reset.pack()

        # władowanie canvasa i bloku komunikatów
        self.__game.set_geometry(self.__canvas, self.__l_stat)

        # ustawienie początkowego komunikatu
        if self.__player:
            self.__game.set_stat("Zaczyna gracz numer 1")
        else:
            if self.__ai_player:
                self.__game.set_stat("Zaczyna komputer...")
            else:
                self.__game.set_stat("Zaczyna gracz numer 2")

        print("władowano geometrie...")

    def start_game(self):
        """Metoda uruchamiająca główną pętle gry."""
        print("otworzono okno gry...")

        self.__game.draw()

        self.__window.mainloop()
        print("zamknięto okno gry")

    def change_player(self, player):
        """Metoda reagująca na przyckiski odpowiedzialne za zmianę gracza."""
        if self.__game.hits > 0:
            return

        if self.__ai_player != player:
            self.__ai_player = player

            if not self.__ai_player:  # gdy zmienimy gracza
                # z komputerowego na rzeczywistego - losujemy jeszcze raz kto zaczyna:
                self.__player = choice([False, True])
                self.__s_diff.config(state=tk.DISABLED)
            else:
                # z rzeczywistego na komputerowego - gracz zawsze zaczyna
                self.__player = True
                self.__s_diff.config(state="readonly")

            self.__game.change_player(self.__player)

    def __bt_hit(self, index):
        """Metoda reagująca na przyciski od wyboru kolumny."""
        self.__rbt_computer["state"] = tk.DISABLED
        self.__rbt_player["state"] = tk.DISABLED
        self.__s_diff.config(state=tk.DISABLED)
        self.__game.hit(index)

    def change_level(self):
        """Metoda reagująca na spinboxa odpoweidzialnego
        za zmianę poziomu umiejętności dla gracza komputerowego."""
        txt = self.__s_diff.get()
        levels = ["Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber"]
        index = levels.index(txt)
        self.__game.change_diff(index)

    def __reset_game(self):
        """Metoda odpowiedzialna za resetowanie stanu gry.

        Resetuje ona ustawienia gry oraz planszy,
        dzięki czemu zamykanie okna nie jest wymagane."""
        del self.__game
        print("zresetowano grę....")
        print()

        print("skonfigurowano okno gry...")

        # tablica z każdym polem
        self.__tpoles = [[0 for col in range(COLS)] for row in range(ROWS)]
        # tablica przechowująca poziomy każdej kolumny
        self.__tlevels = [5 for col in range(COLS)]

        # True  #kto zaczyna gracz 1 czy 2 True - gracz nr 1,
        # False - gracz nr 2, dużo false, bo przekłamuje
        self.__player = choice([True, False])

        self.__game = GameFunctions(self.__window_heigh, self.__window_width,
                                    self.end_game, self.__tpoles, self.__tlevels, self.__player,
                                    self.__ai_player, self.__diff)
        self.change_level()
        if self.__ai_player:
            self.__player = True
        print("władowano dane gry...")

        # funkcje geometrii
        self.__rbt_computer["state"] = tk.ACTIVE
        self.__rbt_player["state"] = tk.ACTIVE
        self.__s_diff.config(state="readonly")
        if self.__ai_player:
            self.__rbt_computer.select()
        else:
            self.__rbt_player.select()

        self.__game.set_geometry(self.__canvas, self.__l_stat)

        # ustawienie początkowego komunikatu
        if self.__player:
            self.__game.set_stat("Zaczyna gracz numer 1")
        else:
            if self.__ai_player:
                self.__game.set_stat("Zaczyna komputer...")
            else:
                self.__game.set_stat("Zaczyna gracz numer 2")

        print("władowano geometrie...")

        print("przeładowano okno gry...")
        self.__game.draw()

    def end_game(self, info):
        """Metoda odpowiedzialna za wyświetlanie dodatkowego okna i kończenie gry."""
        display = ""
        if info == 1:
            display = "Wygrał gracz numer 1"
        elif info == 2:
            display = "Wygrał gracz numer 2"
        elif info == 3:
            display = "Wygrał komputer"
        else:
            display = "Remis"

        message = tk.messagebox.askquestion(title="Connect4",
                                            message=display + " czy chcesz kontynuować?")

        if message == "yes":
            self.__reset_game()
        else:
            self.__window.destroy()

        return display
