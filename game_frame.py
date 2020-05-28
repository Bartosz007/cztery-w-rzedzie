"""Plik przechowujący klasę odpowiadający za odpowiednią budowę okna gry oraz jego elementów."""

import functools
import tkinter as tk
import tkinter.messagebox

import game_mechanics
import players

from utils.constans import Basic, Style, GameStatus

GLOBAL_SCALE = 1
WINDOW_SCALE_W = GLOBAL_SCALE * 0.6
WINDOW_SCALE_H = GLOBAL_SCALE * 0.85


class GameFrame:
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
        print("fd")
        print(int(Basic.COLS))
        board = [[0 for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        levels = [5 for col in range(Basic.COLS)]

        # czy gracz komputerowy jest włączony True - włączony, False - wyłączony
        self.__ai_player = True

        difficulty = 0
        first_player = players.human_player.HumanPlayer(board, levels)
        second_player = players.computer_player.ComputerPlayer(board, levels, difficulty)

        self.__game = game_mechanics.GameMechanics(self.__window_heigh, self.__window_width,
                                                   self.end_game, board, levels, first_player, second_player)

        self.__stat = None
        self.__canvas = None
        self.__rbt_computer = None
        self.__rbt_player = None
        self.__s_diff = None

    def load_geometry(self):
        """Metoda tworząca wszystkie elementy okna gry."""
        # bloki główne
        f_stat_menu = tk.Frame(self.__window, width=self.__window_width,
                               heigh=self.__window_heigh * 0.08, bg=Style.BLUE)
        f_stat_menu.pack_propagate(0)
        f_stat_menu.pack()

        f_top_menu = tk.Frame(self.__window, width=self.__window_width,
                              heigh=self.__window_heigh * 0.07, bg=Style.BLUE)
        f_top_menu.pack_propagate(0)
        f_top_menu.pack()
        f_top_in_menu = tk.Frame(f_top_menu, width=self.__window_width * 0.95,
                                 heigh=self.__window_heigh * 0.07, bg=Style.BLUE)
        f_top_in_menu.pack_propagate(0)
        f_top_in_menu.pack()  # ten blok istnieje, aby nie pojawiały się białe paski z boku

        f_board = tk.Frame(self.__window, width=self.__window_width,
                           heigh=self.__window_heigh * 0.7, bg=Style.BLUE)
        f_board.pack_propagate(0)
        f_board.pack()

        # bloki menu dolneg =-----------------------------------------------
        f_bottom_menu = tk.Frame(self.__window, width=self.__window_width,
                                 heigh=self.__window_heigh * 0.15, bg=Style.BLUE)
        f_bottom_menu.pack_propagate(0)
        f_bottom_menu.pack()

        f_bottom_left = tk.Frame(f_bottom_menu, width=self.__window_width * (2 / 3),
                                 heigh=self.__window_heigh * 0.2, bg=Style.BLUE)
        f_bottom_left.pack_propagate(0)
        f_bottom_left.pack(side=tk.LEFT)

        f_bottom_right = tk.Frame(f_bottom_menu, width=self.__window_width / 3,
                                  heigh=self.__window_heigh * 0.2, bg=Style.BLUE)
        f_bottom_right.pack_propagate(0)
        f_bottom_right.pack(side=tk.RIGHT)

        f_player_menu = tk.Frame(f_bottom_left, width=self.__window_width * (2 / 3),
                                 heigh=self.__window_heigh * 0.1, bg=Style.BLUE)
        f_player_menu.pack()

        f_diff_menu = tk.Frame(f_bottom_left, width=self.__window_width * (2 / 3),
                               heigh=self.__window_heigh * 0.1, bg=Style.BLUE)
        f_diff_menu.pack_propagate(0)
        f_diff_menu.pack()

        f_reset_menu = tk.Frame(f_bottom_right, width=self.__window_width / 3,
                                heigh=self.__window_heigh * 0.2, bg=Style.BLUE)
        f_reset_menu.pack_propagate(0)
        f_reset_menu.pack()

        # panel komunikatów=----------------------------------------------------------
        self.__stat = tk.Label(f_stat_menu, bg=Style.BLUE, text="komunikat",
                               font=(Style.FONT, Style.FONT_SIZE * 2))
        self.__stat.pack(side=tk.TOP)

        # panel przycisków
        fixed_window_width = self.__window_width * 0.95 / 7
        for index in range(Basic.COLS):
            frame = tk.Frame(f_top_in_menu, width=fixed_window_width,
                             heigh=self.__window_heigh * 0.1, bg=Style.BLUE)
            frame.pack_propagate(0)
            frame.pack(side=tk.LEFT)
            button = tk.Button(frame, text="{}".format(index + 1), padx=self.__window_width / 28,
                               pady=self.__window_heigh / 80, bg=Style.ORANGE)
            button.config(command=functools.partial(self.__hit, index))
            button.pack(side=tk.BOTTOM)

        # panel środkowy
        self.__canvas = tk.Canvas(f_board, width=self.__window_width,
                                  height=self.__window_heigh * 0.7)
        self.__canvas.pack()

        # panel Player Menu=-----------------------------------------------------------------
        l_pm = tk.Label(f_player_menu, text="Ustawienia drugiego gracza: ",
                        font=(Style.FONT, Style.FONT_SIZE - 1), bg=Style.BLUE)
        l_pm.pack(side=tk.TOP)

        grup = True
        self.__rbt_computer = tk.Radiobutton(f_player_menu, text="Komputer", variable=grup, value=1,
                                             font=(Style.FONT, Style.FONT_SIZE - 2), indicatoron=0,
                                             bg=Style.ORANGE,
                                             command=lambda: self.change_player(True),
                                             padx=25, pady=2)
        self.__rbt_computer.pack(side=tk.LEFT)

        self.__rbt_player = tk.Radiobutton(f_player_menu, text="Człowiek", variable=grup, value=2,
                                           font=(Style.FONT, Style.FONT_SIZE - 2), indicatoron=0,
                                           bg=Style.ORANGE,
                                           command=lambda: self.change_player(False),
                                           padx=25, pady=2)
        self.__rbt_player.pack(side=tk.RIGHT)

        if self.__ai_player:
            self.__rbt_computer.select()
        else:
            self.__rbt_player.select()

        # panel Diff Menu=------------------------------------------------
        l_dm = tk.Label(f_diff_menu, width=int(self.__window_width / 20), bg=Style.BLUE,
                        text="Poziom trudności: ", font=(Style.FONT, Style.FONT_SIZE - 1))
        l_dm.pack(side=tk.TOP)
        levels = ("Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber")
        self.__s_diff = tk.Spinbox(f_diff_menu, width=int(self.__window_width / 25), bg=Style.BLUE,
                                   justify=tk.CENTER, values=levels,
                                   font=(Style.FONT, Style.FONT_SIZE), state="readonly")
        self.__s_diff.config(command=self.change_difficulty)
        self.__s_diff.pack(side=tk.BOTTOM)

        # panel Reset
        bt_reset = tk.Button(f_reset_menu, text="Reset", padx=int(self.__window_width / 30),
                             pady=self.__window_heigh, font=(Style.FONT, Style.FONT_SIZE + 5), bg=Style.ORANGE)
        bt_reset.config(command=self.__reset_game)
        bt_reset.pack()

        # władowanie canvasa i bloku komunikatów
        self.__game.set_geometry(self.__canvas, self.__stat)

        # ustawienie początkowego komunikatu
        # if self.__player:
        self.__game.set_stat("Zaczyna gracz numer 1")
        #  else:
        #      if self.__ai_player:
        #          self.__game.set_stat("Zaczyna komputer...")
        #      else:
        #           self.__game.set_stat("Zaczyna gracz numer 2")

        print("władowano geometrie...")

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
                self.__s_diff.config(state=tk.DISABLED)
            else:
                self.__s_diff.config(state="readonly")
                self.__game.change_diff(self.__s_diff.get())

            self.__game.change_player()

    def change_difficulty(self):
        """Metoda reagująca na spinboxa odpowiedzialnego
        za zmianę poziomu umiejętności dla gracza komputerowego."""

        self.__game.change_diff(self.__s_diff.get())

    def end_game(self, info):
        """Metoda odpowiedzialna za wyświetlanie dodatkowego okna i kończenie gry."""
        print(info)
        display = ""
        if info == GameStatus.PLAYER_ONE_WON:
            display = "Wygrał gracz numer 1"
        elif info == GameStatus.PLAYER_TWO_WON:
            display = "Wygrał gracz numer 2"
        elif info == GameStatus.COMPUTER_WON:
            display = "Wygrał komputer"
        else:
            display = "Remis"

        message = tk.messagebox.askquestion(title="Connect4",
                                            message="{} czy chcesz kontynuować?".format(display))

        if message == "yes":
            self.__reset_game()
        else:
            self.__window.destroy()

        return display

    def __reset_game(self):
        """Metoda odpowiedzialna za resetowanie stanu gry.

        Resetuje ona ustawienia gry oraz planszy,
        dzięki czemu zamykanie okna nie jest wymagane."""
        new_second_player = isinstance(self.__game.second_player, players.computer_player.ComputerPlayer)
        del self.__game
        print("zresetowano grę....")
        print()

        board = [[0 for col in range(Basic.COLS)] for row in range(Basic.ROWS)]
        levels = [5 for col in range(Basic.COLS)]

        difficulty = 0
        first_player = players.human_player.HumanPlayer(board, levels)

        if new_second_player:
            diffs = ["Losowy", "Łatwy", "Też łatwy", "Średni", "Trudny", "Bardzo trudny", "Uber"]
            index = diffs.index(self.__s_diff.get())
            second_player = players.computer_player.ComputerPlayer(board, levels, index)
        else:
            second_player = players.human_player.HumanPlayer(board, levels)

        self.__game = game_mechanics.GameMechanics(self.__window_heigh, self.__window_width,
                                                   self.end_game, board, levels, first_player, second_player)

        print("władowano dane gry...")

        # funkcje geometrii
        self.__rbt_computer["state"] = tk.ACTIVE
        self.__rbt_player["state"] = tk.ACTIVE
        self.__s_diff["state"] = "readonly"

        if new_second_player:
            self.__rbt_computer.select()
        else:
            self.__rbt_player.select()

        self.__game.set_geometry(self.__canvas, self.__stat)

        # ustawienie początkowego komunikatu
        self.__game.set_stat("Zaczyna gracz numer 1")

        print("władowano geometrie...")

        print("przeładowano okno gry...")
        self.__game.draw()

    def __hit(self, index):
        """Metoda reagująca na przyciski od wyboru kolumny."""
        self.__rbt_computer["state"] = tk.DISABLED
        self.__rbt_player["state"] = tk.DISABLED
        self.__s_diff["state"] = tk.DISABLED
        self.__game.hit(index)
