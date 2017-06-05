import numpy as np

gameBoard = np.array([[{"colour": "black"}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}],
                      [{"colour": None}, {"colour": "red"}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}],
                      [{"colour": None}, {"colour": None}, {"colour": "black"}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}],
                      [{"colour": None}, {"colour": None}, {"colour": None}, {"colour": "black"}, {"colour": None}, {"colour": None}, {"colour": None}],
                      [{"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": "black"}, {"colour": None}, {"colour": None}],
                      [{"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": None}, {"colour": "black"}, {"colour": None}]])


def checkBoard(board):
    # ROWS

    redCounter = 0
    blackCounter = 4

    for row in board:
        for cell in row:
            if cell["colour"] == "red":
                redCounter += 1
                blackCounter = 0
                if redCounter >= 4:
                    return "red wins"
            elif cell["colour"] == "black":
                redCounter = 0
                blackCounter += 1
                if blackCounter >= 4:
                    return "black wins"
            else:
                redCounter = 0
                blackCounter = 0

        redCounter = 0
        blackCounter = 0

    redCounter = 0
    blackCounter = 0

    # COLUMNS

    for column in board.transpose():
        for cell in column:
            if cell["colour"] == "red":
                redCounter += 1
                blackCounter = 0
                if redCounter >= 4:
                    return "red wins"
            elif cell["colour"] == "black":
                redCounter = 0
                blackCounter += 1
                if blackCounter >= 4:
                    return "black wins"
            else:
                redCounter = 0
                blackCounter = 0

        redCounter = 0
        blackCounter = 0

    redCounter = 0
    blackCounter = 0

    # DIAGONAL 1

    yCounter = 2
    xCounter = 0

    for cell in range(0, 4):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter += 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 1
    xCounter = 0

    for cell in range(0, 5):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter += 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 0
    xCounter = 0

    for cell in range(0, 6):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter += 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 0
    xCounter = 1

    for cell in range(0, 6):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter += 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 0
    xCounter = 2

    for cell in range(0, 5):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter += 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 0
    xCounter = 3

    for cell in range(0, 4):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter += 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    # DIAGONAL 2

    yCounter = 5
    xCounter = 3

    for cell in range(0, 4):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0
        yCounter -= 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 5
    xCounter = 2

    for cell in range(0, 5):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0
        yCounter -= 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 5
    xCounter = 1

    for cell in range(0, 6):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter -= 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 5
    xCounter = 0

    for cell in range(0, 6):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter -= 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 4
    xCounter = 0

    for cell in range(0, 5):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter -= 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    yCounter = 3
    xCounter = 0

    for cell in range(0, 4):
        if board[yCounter][xCounter]["colour"] == "red":
            redCounter += 1
            blackCounter = 0
            if redCounter >= 4:
                return "red wins"
        elif board[yCounter][xCounter]["colour"] == "black":
            redCounter = 0
            blackCounter += 1
            if redCounter >= 4:
                return "black wins"
        else:
            redCounter = 0
            blackCounter = 0

        yCounter -= 1
        xCounter += 1

    redCounter = 0
    blackCounter = 0

    return "continue game"

print(checkBoard(gameBoard))
