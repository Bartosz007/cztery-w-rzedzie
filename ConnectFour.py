from random import choice
from functools import partial
from tkinter import *
from GameFunctions import *


class ConnectFour:
    def __init__(self,window):  
        self.__COLS = 7 #kolumny 
        self.__ROWS = 6 #wiersze 
        GLOBAL_SCALE = 1
        WINDOW_SCALE_W = GLOBAL_SCALE * 0.6   #rozmiar okna- szerokość skala 6:10
        WINDOW_SCALE_H = GLOBAL_SCALE * 0.85    #rozmiar okna- wysokość skala 6:10
        SCREEN_HEIGH = window.winfo_screenheight() #rozdzielczość ekranu
        SCREEN_WIDTH = window.winfo_screenwidth()
              
        self.__window = window
        self.__window_heigh = int( SCREEN_HEIGH * WINDOW_SCALE_H )
        self.__window_width = int( SCREEN_WIDTH * WINDOW_SCALE_W )
        self.__window.geometry("{}x{}+{}+{}".format(
            int(self.__window_width),
            int(self.__window_heigh),
            int(self.__window_width * 0.3),
            int(self.__window_heigh * 0.08))) # rozmiar okna i pozycja po uruchomeniu

        self.__game = GameFunctions(self.__COLS,self.__ROWS, self.__window_heigh,self.__window_width,self.__endGame)

        print("skonfigurowano okno gry...")

    def loadData(self):
        self.__tpoles = [[0 for col in range(self.__COLS)] for row in range(self.__ROWS)] #tablica z każdym polem
        self.__tlevels = [5 for col in range(self.__COLS)]  #tablica przechowująca poziomy każdej kolumny
        self.__player = choice([True,False])#True  #kto zaczyna gracz 1 czy 2 True - gracz nr 1, False - gracz nr 2, dużo false, bo przekłamuje
        #self.__aiPlayer = False  # czy gracz komputerowy jest włączony True - włączony, False - wyłączony
        self.__aiPlayer = True  # czy gracz komputerowy jest włączony True - włączony, False - wyłączony
        self.__diff = 0 # poziom trudnosci sztucznej inteligencji 0-7
        self.__game.loadData(self.__tpoles,self.__tlevels,self.__player,self.__aiPlayer,self.__diff)
        
        if self.__aiPlayer: # warunek, że jeśli gramy z komputerem, to zawsze gracz zaczyna
            self.__player = True

        print("władowano dane gry...")

    def loadGeometry(self):
        FONT = "Times New Roman"
        FONT_SIZE = 15
        COLOR = "#296380"
        SEC_COLOR = "#6C858A"
        #bloki główne
        fStatMenu = Frame(self.__window ,width=self.__window_width ,heigh=self.__window_heigh*0.08,bg=COLOR)
        fStatMenu.pack_propagate(0)
        fStatMenu.pack()

        fTopMenu = Frame(self.__window ,width=self.__window_width ,heigh=self.__window_heigh*0.07,bg=COLOR)
        fTopMenu.pack_propagate(0)
        fTopMenu.pack()    
        fTopInMenu = Frame(fTopMenu ,width=self.__window_width *0.95 ,heigh=self.__window_heigh*0.07,bg=COLOR)
        fTopInMenu.pack_propagate(0)
        fTopInMenu.pack() #ten blok istnieje, aby nie pojawiały się białe paski z boku
        

        fBoard = Frame(self.__window,width=self.__window_width,heigh=self.__window_heigh*0.7,bg=COLOR)
        fBoard.pack_propagate(0)
        fBoard.pack()

        #bloki menu dolneg =-------------------------------------------------------------------------------------
        fBottomMenu = Frame(self.__window,width=self.__window_width,heigh=self.__window_heigh*0.15,bg=COLOR)
        fBottomMenu.pack_propagate(0)
        fBottomMenu.pack()

        fBottomLeft = Frame(fBottomMenu,width=self.__window_width*(2/3),heigh=self.__window_heigh*0.2,bg=COLOR)
        fBottomLeft.pack_propagate(0)
        fBottomLeft.pack(side = LEFT)

        fBottomRight = Frame(fBottomMenu,width=self.__window_width/3,heigh=self.__window_heigh*0.2,bg=COLOR)
        fBottomRight.pack_propagate(0)
        fBottomRight.pack(side = RIGHT)

        fPlayerMenu = Frame(fBottomLeft,width=self.__window_width*(2/3),heigh=self.__window_heigh*0.1,bg=COLOR)
        fPlayerMenu.pack()

        fDiffMenu = Frame(fBottomLeft,width=self.__window_width*(2/3),heigh=self.__window_heigh*0.1,bg=COLOR)
        fDiffMenu.pack_propagate(0)
        fDiffMenu.pack()

        fResetMenu = Frame(fBottomRight,width=self.__window_width/3,heigh=self.__window_heigh*0.2,bg=COLOR)
        fResetMenu.pack_propagate(0)
        fResetMenu.pack()

        #panel komunikatów=--------------------------------------------------------------------------------------
        self.__lStat = Label(fStatMenu, bg=COLOR,text="komunikat",font=(FONT, FONT_SIZE*2))
        self.__lStat.pack(side=TOP)
        
        #panel przycisków    
        w=self.__window_width*0.95/7    
        for index in range(self.__COLS):
            fr = Frame(fTopInMenu,width=w,heigh=self.__window_heigh*0.1,bg=COLOR)
            fr.pack_propagate(0)
            fr.pack(side=LEFT)
            bt = Button(fr, text="{}".format(index+1),padx=self.__window_width/28,pady=self.__window_heigh/80,bg="#D15304")
            bt.config(command = partial(self.__btHit, index))
            bt.pack(side=BOTTOM)

       
        #panel środkowy
        self.__canvas = Canvas(fBoard, width=self.__window_width, height=self.__window_heigh*0.7)
        self.__canvas.pack()

        #panel Player Menu=-----------------------------------------------------------------
      #  btReset = Button(fBottomMenu,)

        lPM=Label(fPlayerMenu,text="Ustawienia drugiego gracza: ",font=(FONT, FONT_SIZE-1),bg=COLOR)
        lPM.pack(side=TOP)

        grup = True
        self.__rbtComputer = Radiobutton(fPlayerMenu, text="Komputer", variable = grup, value = 1, font=(FONT, FONT_SIZE-2), 
                                         indicatoron=0, bg="#D15304", command = lambda : self.changePlayer(True),padx=25,pady=2)
        self.__rbtComputer.pack(side=LEFT)

        self.__rbtPlayer = Radiobutton(fPlayerMenu, text="Człowiek", variable = grup, value = 2, font=(FONT, FONT_SIZE-2),
                                      indicatoron=0, bg="#D15304",command = lambda : self.changePlayer(False),padx=25,pady=2)  
        self.__rbtPlayer.pack(side = RIGHT)
        if self.__aiPlayer:
            self.__rbtComputer.select()    
        else:
            self.__rbtPlayer.select()
        #panel Diff Menu=-------------------------------------------------------------------------------

        lDM=Label(fDiffMenu,width = int(self.__window_width/20),bg=COLOR,text="Poziom trudności: ",font=(FONT, FONT_SIZE-1))
        lDM.pack(side=TOP)
        levels = ("Losowy", "Łatwy", "Też łatwy","Średni","Trudny","Bardzo trudny","Uber")
        self.__sDiff = Spinbox(fDiffMenu,width=int(self.__window_width/25),bg=COLOR,justify=CENTER,values=levels,font=(FONT, FONT_SIZE),state="readonly")
        self.__sDiff.config(command = self.changeLevel)
        self.__sDiff.pack(side=BOTTOM)

        #panel Reset
        btReset = Button(fResetMenu, text="Reset",padx=int(self.__window_width/30),pady=self.__window_heigh,font=(FONT, FONT_SIZE+5),bg="#D15304")
        btReset.config(command=self.__resetGame)
     #   btReset.config(command=self.test)
        btReset.pack()

        #władowanie canvasa i bloku komunikatów
        self.__game.setGeometry(self.__canvas,self.__lStat)
        
        #ustawienie początkowego komunikatu
        if self.__player:
            self.__game.setStat("Zaczyna gracz numer 1")
        else:
            if self.__aiPlayer:
                self.__game.setStat("Zaczyna komputer...")
            else:
                self.__game.setStat("Zaczyna gracz numer 2")

        print("władowano geometrie...")

    def startGame(self):
        print("otworzono okno gry...")

        self.__game.draw()       

        self.__window.mainloop()
        print("zamknięto okno gry")
    
    def changePlayer(self, player):
        if self.__game.hits > 0:
            self.setStat("Nie można zmienić gracza w trakcie rozgrywki...")
            return

        if self.__aiPlayer != player:
            self.__aiPlayer = player

            if self.__aiPlayer == False:#gdy zmienimy gracza
                self.__player = choice([False,True]) # z komputerowego na rzeczywistego - losujemy jeszcze raz kto zaczyna
                self.__sDiff.config(state = DISABLED)
            else:
                self.__player = True # z rzeczywistego na komputerowego - gracz zawsze zaczyna
                self.__sDiff.config(state = "readonly")

            self.__game.changePlayer(self.__player)

    def __btHit(self,index):
        self.__rbtComputer["state"]=DISABLED
        self.__rbtPlayer["state"]=DISABLED
        self.__sDiff.config(state = DISABLED)
        self.__game.hit(index)

    def changeLevel(self):
        txt = self.__sDiff.get()
        levels = ["Losowy", "Łatwy", "Też łatwy","Średni","Trudny",
                        "Bardzo trudny","Uber"]
        a = levels.index(txt)
        self.__game.changeDiff(a)

    def __resetGame(self):#tu dorobić pmenu przesuwane z poziomami trudności
        del self.__game
        print("zresetowano grę....")
        print()
        
        #funkcje init
        self.__game = GameFunctions(self.__COLS,self.__ROWS, self.__window_heigh,self.__window_width,self.__endGame)
        print("skonfigurowano okno gry...")

        #funkcje wczytania danych
        self.__tpoles = [[0 for col in range(self.__COLS)] for row in range(self.__ROWS)] #tablica z każdym polem
        self.__tlevels = [5 for col in range(self.__COLS)]  #tablica przechowująca poziomy każdej kolumny
        self.__player = choice([True,False])#True  #kto zaczyna gracz 1 czy 2 True - gracz nr 1, False - gracz nr 2, dużo false, bo przekłamuje

        self.__game.loadData(self.__tpoles,self.__tlevels,self.__player,self.__aiPlayer,self.__diff)
        self.changeLevel()
        if self.__aiPlayer:
            self.__player = True
        print("władowano dane gry...")
             

        #funkcje geometrii
        self.__rbtComputer["state"]=ACTIVE
        self.__rbtPlayer["state"]=ACTIVE
        self.__sDiff.config(state = "readonly")
        if self.__aiPlayer:
            self.__rbtComputer.select()   
        else:
            self.__rbtPlayer.select()

        self.__game.setGeometry(self.__canvas,self.__lStat)
        
        #ustawienie początkowego komunikatu
        if self.__player:
            self.__game.setStat("Zaczyna gracz numer 1")
        else:
            if self.__aiPlayer:
                self.__game.setStat("Zaczyna komputer...")
            else:
                self.__game.setStat("Zaczyna gracz numer 2")

        print("władowano geometrie...")

        print("przeładowano okno gry...")
        self.__game.draw()  

    def __endGame(self,info):
        display = ""
        if info == True:
            display = "Wygrał gracz numer 1"
        elif info == False:
            display = "Wygrał gracz numer 2"
        elif info == 3:
            display = "Wygrał komputer"
        else:
            display = "Remis"

        v = messagebox.askquestion(title="Connect4", message = display + " czy chcesz kontynuować?")

        if v =="yes":
            self.__resetGame()
        else:
            self.__window.destroy()

        


