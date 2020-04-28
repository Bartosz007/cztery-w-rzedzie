from tkinter import *
from functools import partial
from ConnectFour import *

def main():



    window = Tk()
    window.title( "Cztery w rzędzie" ) #napis na oknie

    game = ConnectFour(window) 

    game.loadData()
    game.loadGeometry()
    game.startGame()
    

   # game.test()
   # game.test()

if __name__ == "__main__":
    main()
  
