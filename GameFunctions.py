from time import sleep
from functools import partial
from AI import ai
from tkinter import messagebox,PhotoImage

class GameFunctions():
    def __init__(self,cols,rows,heigh,width,endgame):#jak wartosci w tablicach nie beda się zmieniac to ununąć konstruktor
        self.__cols  = cols
        self.__rows = rows      
        self.__heigh = heigh
        self.__width = width
        self.hits = 0
        self.__endGame = endgame
        print("{}x{}".format(cols,rows))

    def loadData(self,tpoles,tlevels,player,aiplayer,diff):
        self.__tpoles = tpoles
        self.__tlevels = tlevels
        self.__player = player
        self.__aiPlayer = aiplayer
        self.__diff = diff#poziom trudności bota
           
    def setGeometry(self,canvas,fStat):
        self.__canvas = canvas
        self.__fStat = fStat

    def draw(self):
        self.__canvas.delete("all")
        
        self.__canvas.create_rectangle(0, 0, self.__width,self.__heigh * 0.7, fill="#8A3500")

        rect_heigh=(self.__heigh * 0.60/ self.__rows)
        rect_width=rect_heigh
        heigh_hole = (self.__heigh * 0.7 -(rect_heigh*6))/7#7odstępów
        width_hole = (self.__width -(rect_heigh*7))/8 # 8 odstępów
      
        for i in range(self.__rows):   
            for j in range(self.__cols):
                color = "white"
                if self.__tpoles[i][j] == -1:
                    color = "#FF2200"
                elif self.__tpoles[i][j] == 1:
                    color = "#FF9B21"

                self.__canvas.create_oval(width_hole* (1+j)+rect_width * (1+j),
                                          heigh_hole* (1+i)+rect_heigh * (1+i),
                                          width_hole* (1+j)+rect_width * j,
                                          heigh_hole* (1+i)+rect_heigh * i,
                                          fill = color ,outline = color)

    def hit(self,col):
        if self.__aiPlayer:#jeśli gramy z komputerem
            self.__aicalculate(col)
        else:
            self.__calculate(col)

    def changePlayer(self,player):
        self.__player = player

        if self.__aiPlayer:
            if self.__player:
                self.setStat("Zaczyna gracz numer 1")
            else:
                self.setStat("Zaczyna gracz numer 2")

        else:
            self.setStat("Zaczyna gracz numer 1")



         
        self.__aiPlayer = not self.__aiPlayer
         
    def changeDiff(self,newDiff):
        self.__diff = newDiff

    def setStat(self,text): #wyświetla komunikat o podanej treści
                
        old = self.__fStat["text"]     
        
        self.__fStat["text"] = text

    def __calculate(self, col):
      #  print(self.__tlevels)
        row = self.__tlevels[col]

        if row < 0:
            self.setStat("Brak miejsca w tej kolumnie, strzel ponownie...")
            return

        status = False
        if self.__player:#gracz nr 1 
            self.__tpoles[row][col] = -1
            self.setStat("Tura gracza 2")#jeśli gramy z graczem drugim

            status = self.__check(row,col,-1)
            if status:
                #funckja z kończeniem gry
                self.setStat("Wygrał gracz numer 1")
         
        else:
            self.__tpoles[row][col]=1#gracz nr 2

            self.setStat("Tura gracza 1")
            status = self.__check(row,col,1)
            if status: #funckja z kończeniem gry
                self.setStat("Wygrał gracz numer 2")
                

        self.draw()

        if status:
            self.__endGame(self.__player)

        self.hits = self.hits + 1        
        if self.hits > 41:
            self.__endGame(4)
        
        self.__tlevels[col] = self.__tlevels[col] - 1
        self.__player = not self.__player
        
    def __aicalculate(self,col):
        #---------------sekcja gracza---------------------

        row = self.__tlevels[col]
        
        status = False
        if row < 0:
            self.setStat("Brak miejsca w tej kolumnie, strzel ponownie...")
            return

        self.__tpoles[row][col] = -1

        status = self.__check(row,col,-1)
        if status:
            self.setStat("Wygrał gracz numer 1")
            print("wygrał gracz 1")
                        #funckja z kończeniem gry
        
        self.__tlevels[col] = self.__tlevels[col] - 1

        self.draw()

        if status:
            self.__endGame(True)
            return

        self.hits = self.hits + 1
        if self.hits > 41:
            self.setStat("Remis")            
            self.__endGame(4)
            return
        
        self.setStat("Komputer myśli...")

        #---------------sekcja komputera---------------------

       
        col2 = ai(self.__tpoles,self.__tlevels,self.__rows,self.__cols,self.__diff)#strzał komputera
        row2 = self.__tlevels[col2]
       # row2,col2 = ai(self.__tpoles,self.__tlevels,self.__rows,self.__cols)
       
        self.__tpoles[row2][col2] = 1

        status = self.__check(row2,col2,1)
        if status: #funckja z kończeniem gry
            self.setStat("Wygrał komputer...")
            print("wygrał komputer")
        
        self.__tlevels[col2] = self.__tlevels[col2] - 1
        self.draw()

        if status:
            self.__endGame(3)
            return

        self.hits = self.hits + 1
        if self.hits > 41:
            self.setStat("Remis")
            self.__endGame(4)
            return

        self.setStat("Tura gracza 1")

    def __check(self,row,col,sign):#przebudować - pozbyć się rekurencji
        counter = 0
        for i in range(self.__cols):        
            if self.__tpoles[row][i] == sign:
                counter = counter + 1
                if counter == 4:
                    return True
            else:
                counter=0

        counter = 0
        for i in range(self.__rows):        
            if self.__tpoles[i][col] == sign:
                counter = counter + 1
                if counter == 4:
                    return True
            else:
                counter=0

        #przekątna od lewej góra do prawej dół
        if col > row:
            eqal = row
        else:
            eqal = col
        brow = abs(eqal - row)
        bcol = abs(eqal - col)
      #  print("strzaŁ: "+str(row)+" "+str(col)+" kto: "+ str(sign))
        counter = 0
        while brow < 6 and bcol <7:
            if self.__tpoles[brow][bcol] == sign:
                counter = counter + 1
                if counter == 4:
                    return True
            else:
                counter=0
            brow = brow + 1
            bcol = bcol + 1

        #przekątna od prawej góra do lewej dół
        if (col+row)<7:
            bcol = col+row
            brow = 0
        else:
            bcol = 6            
            brow = row - (6 - col)
        counter = 0
        while brow < 6 and bcol >= 0:
            
            if self.__tpoles[brow][bcol] == sign:
                counter = counter + 1
           #     print(counter,brow,bcol)
                if counter == 4:
                    return True
            else:
                counter=0

            brow = brow + 1
            bcol = bcol - 1

        return False
     
    def __del__(self):
        print("destruktor")

