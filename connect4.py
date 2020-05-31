"""Główny plik projektowy"""

import tkinter as tk

import game_frame


def main():
    """Główna funkcja gry"""

    tk.window = tk.Tk()
    tk.window.title("Cztery w rzędzie")  # napis na oknie

    game = game_frame.GameFrame(tk.window)
    game.start_game()


if __name__ == "__main__":
    main()
