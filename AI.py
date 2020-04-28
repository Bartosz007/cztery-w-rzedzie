from random import randint,choice
import time

ROWS = 1
COLS = 1

def ai(tpoles,tlevels,trows,tcols,diff):
    global ROWS,COLS
    ROWS = trows
    COLS = tcols

    ctpoles=[[tpoles[row][col] for col in range(COLS)]for row in range(ROWS)]
    ctlevels=[tlevels[x] for x in range(COLS)]

    for i in range(ROWS):
        for j in range(COLS):
            if ctpoles[i][j] == 2:
                pass
             #   ctpoles[i][j] = 1
            elif ctpoles[i][j] == 1:
                pass
           #    ctpoles[i][j] = -1
            
    print("Poziom trudności: "+str(diff))
    fields = rightFields(tpoles,tlevels)
    if diff == 0 :
        return losowanie(fields)
    else:
        col,score = minimax3(ctpoles,ctlevels,diff,True)#diff jako poziom zagłębienia funckji
        return col

def rightFields(tpoles,tlevels):
 
    tab = []
    for i in range(len(tlevels)):
        if tlevels[i] >= 0:
            tab.append((tlevels[i],i))

    return tab

def losowanie(fields):
    r = randint(0,len(fields)-1)
  #  row,col = fields[r]
    # return col
    return fields[r][1] #zwraca to krotkę(drugi elelemnt)

def minimax3(tpoles,tlevels,depth,maximazing):
    fields = rightFields(tpoles,tlevels)
    if depth == 0 or len(fields)==0:
        return (None,score_board(tpoles))
    if maximazing:
        value = -999999999
        column = 1
        for row,col in fields:
            ctpoles=[[tpoles[r][c] for c in range(COLS)]for r in range(ROWS)]
            ctlevels=[tlevels[x] for x in range(COLS)]

            ctpoles[row][col] = 1
            ctlevels[col]=ctlevels[col] - 1 

            c,score = minimax3(ctpoles,ctlevels,depth-1,False)
            if score>value:
                value = score
                column = col

        return column,value
    else:
        value = 999999999
        column = 1
        for row,col in fields:
            ctpoles=[[tpoles[r][c] for c in range(COLS)]for r in range(ROWS)]
            ctlevels=[tlevels[x] for x in range(COLS)]

            ctpoles[row][col] = -1 
            ctlevels[col]=ctlevels[col] - 1 

            c,score = minimax3(ctpoles,ctlevels,depth-1,True)
            if score < value:
                value = score
                column = col

        return column,value

def score_board(tpoles):
    pos = [0 for i in range(9)]

    for i in range(ROWS):
        score = 0
        for j in range(3):
            score = score + tpoles[i][j] 

        for j in range(3, COLS):
            score = score + tpoles[i][j]
            pos[score + 4] = pos[score + 4] + 1

            score = score -  tpoles[i][j - 3]


    for i in range(COLS):
        score = 0
        for j in range(3):
            score = score + tpoles[j][i] 

        for j in range(3, ROWS):
            score = score + tpoles[j][i]
            pos[score + 4] = pos[score + 4] + 1

            score = score - tpoles[j - 3][i]


    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            score = 0

            for shift in range(4):
                y = i + shift
                x = j + shift
                score = score - score + tpoles[y][x]

            pos[score + 4] = pos[score + 4]+ 1


    for i in range(3, ROWS):
        for j in range(COLS - 3):
            score = 0

            for shift in range(4):
                y = i - shift
                x = j + shift
                score = score + tpoles[y][x]

            pos[score + 4] = pos[score + 4]+ 1
    
    player =  0 * pos[0] + 5 * pos[1] + 2 * pos[2] + pos[3]
    computer = pos[5] + 2 * pos[6] + 5 * pos[7] + 0 * pos[8]
    #ogromne znaczenie mają pozycje pos[1] i pos[6]

    if pos[0]!=0:
        return -3333333333333333333
    elif pos[8]!=0:
        return 5555555555555555554
    else:
        return computer-player
    




