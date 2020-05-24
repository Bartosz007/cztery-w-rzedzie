import tkinter as tk

import okno_gry

import gracz_komputerowy

def main():

    tk.window = tk.Tk()
    tk.window.title("Cztery w rzędzie") #napis na oknie

    game = okno_gry.ConnectFour(tk.window)

    #  game.loadData()

    game.load_geometry()
    game.start_game()

    print(gracz_komputerowy.__doc__)

if __name__ == "__main__":
    main()
