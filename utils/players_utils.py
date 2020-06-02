"""Plik zawierający funkcje używane przez klasy players"""

import random

from utils.constants import Basic

INF = 99999999999999


def right_fields(levels):
    """Funkcja zwracająca możliwe pola strzału."""
    tab = []
    for i, value in enumerate(levels):
        if value >= 0:
            tab.append((value, i))

    return tab


def random_field(fields):
    """Funkcja losująca pole strzału."""

    rand = random.randint(0, len(fields) - 1)
    return fields[rand][1]


def score_board(board):
    """Funkcja oceniająca aktualny stan planszy.

    Analizuje aktualny stan planszy i zwraca ocenę."""
    pos = [0 for i in range(9)]

    for i in range(Basic.NUM_ROWS):
        score = 0
        for j in range(3):
            score += board[i][j]

        for j in range(3, Basic.NUM_COLUMNS):
            score += board[i][j]
            pos[score + 4] += + 1

            score -= board[i][j - 3]

    for i in range(Basic.NUM_COLUMNS):
        score = 0
        for j in range(3):
            score += board[j][i]

        for j in range(3, Basic.NUM_ROWS):
            score += board[j][i]
            pos[score + 4] += 1

            score -= board[j - 3][i]

    for i in range(Basic.NUM_ROWS - 3):
        for j in range(Basic.NUM_COLUMNS - 3):
            score = 0

            for shift in range(4):
                row = i + shift
                col = j + shift
                score -= board[row][col]

            pos[score + 4] += 1

    for i in range(3, Basic.NUM_ROWS):
        for j in range(Basic.NUM_COLUMNS - 3):
            score = 0

            for shift in range(4):
                row = i - shift
                col = j + shift
                score += board[row][col]

            pos[score + 4] += 1

    player = 0 * pos[0] + 5 * pos[1] + 2 * pos[2] + pos[3]
    computer = pos[5] + 2 * pos[6] + 5 * pos[7] + 0 * pos[8]
    # ogromne znaczenie mają pozycje pos[1] i pos[6]

    if pos[0] != 0:
        return -3333333333333333333
    elif pos[8] != 0:
        return 5555555555555555554
    else:
        return computer - player


def start_data():
    """Funkcja zwraacjąca domyślne tablice

    Zwraca początkowe tablice wymagane do dalszej gry"""
    board = [[Basic.EMPTY_POSITION for col in range(Basic.NUM_COLUMNS)] for row in range(Basic.NUM_ROWS)]
    levels = [Basic.DEFAULT_POSITION for col in range(Basic.NUM_COLUMNS)]

    return board, levels


def copy_data(board, levels):
    """Funkcja zwraca kopie podanych w parametrach tablic"""
    c_board = [[board[r][c] for c in range(Basic.NUM_COLUMNS)] for r in range(Basic.NUM_ROWS)]
    c_levels = [levels[x] for x in range(Basic.NUM_COLUMNS)]
    return c_board, c_levels


def minimax(board, levels, depth, maximazing):
    """Funkcja wybierająca najoptymalniejsze pole strzału algorytmem minimax."""
    fields = right_fields(levels)
    if depth == 0 or len(fields) == 0:
        return None, score_board(board)
    if maximazing:
        value = -INF
        column = 1
        for row, col in fields:
            c_board, c_levels = copy_data(board, levels)

            c_board[row][col] = Basic.COIN
            c_levels[col] -= 1
            score = minimax(c_board, c_levels, depth - 1, False)[1]
            if score > value:
                value = score
                column = col

        return column, value

    else:
        value = INF
        column = 1
        for row, col in fields:
            c_board, c_levels = copy_data(board, levels)

            c_board[row][col] = -Basic.COIN
            c_levels[col] -= 1

            score = minimax(c_board, c_levels, depth - 1, True)[1]
            if score < value:
                value = score
                column = col

        return column, value


def check(board, row, col, sign):
    """Funkcja sprawdzająca stan gry."""
    counter = 0
    for i in range(Basic.NUM_COLUMNS):
        if board[row][i] == sign:
            counter += 1
            if counter == 4:
                return True
        else:
            counter = 0

    counter = 0
    for i in range(Basic.NUM_ROWS):
        if board[i][col] == sign:
            counter += 1
            if counter == 4:
                return True
        else:
            counter = 0

        # przekątna od lewej góra do prawej dół
    if col > row:
        eqal = row
    else:
        eqal = col
    brow = abs(eqal - row)
    bcol = abs(eqal - col)

    counter = 0
    while brow < Basic.NUM_ROWS and bcol < Basic.NUM_COLUMNS:
        if board[brow][bcol] == sign:
            counter += 1
            if counter == 4:
                return True
        else:
            counter = 0
        brow += 1
        bcol += 1

        # przekątna od prawej góra do lewej dół
    if (col + row) < Basic.NUM_COLUMNS:
        bcol = col + row
        brow = 0
    else:
        bcol = Basic.NUM_ROWS
        brow = row - (Basic.NUM_ROWS - col)
    counter = 0
    while brow < Basic.NUM_ROWS and bcol >= 0:
        if board[brow][bcol] == sign:
            counter += 1
            if counter == 4:
                return True
        else:
            counter = 0

        brow += 1
        bcol -= 1

    return False
