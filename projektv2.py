"""Główny plik projektowy"""

import tkinter as tk

import okno_gry


def main():
    """Główna funkcja gry"""

    tk.window = tk.Tk()
    tk.window.title("Cztery w rzędzie")  # napis na oknie

    game = okno_gry.ConnectFour(tk.window)

    game.load_geometry()
    game.start_game()


if __name__ == "__main__":
    main()
