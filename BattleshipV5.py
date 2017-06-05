"""
PSEUDOCODE:

create player and opponent boards
create player with no positioning
create and position opponent ships

while game loop:
    for every event:
        if close button pressed:
            close game
        if left click down:
            if left click on ship:
                drag ship
        if R is pressed:
            rotate ship:
                if dragging ship:
        if left click up:
            if dragging ship:
                if ship on board:
                    place ship on board
                else:
                    return ship to start

    if all ships have been placed:
        change game state to start game

    blit background image
    blit boards
"""

import pygame
from pygame.locals import *
import numpy as np
from BattleShipLibrary import *

# Initial setup of game

pygame.init()

# Get the resolution of the screen to make the game the same size
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)

# Size of each cell
cellSize = (int(screenSize[0]) / 24, int(screenSize[0] / 24))

# Size of each board
boardSize = (cellSize[0] * 10, cellSize[1] * 10)

# Setting up the screen
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("BATTLESHIP")

# Ocean background
background = pygame.image.load("resources/TopDownOcean.jpg")
background = background.convert()

confirmShipsButton = Sprite(cellSize[0] * 6, cellSize[1] * 12, int(cellSize[0]) * 4, int(cellSize[1]))

gameLoop = True

# gameState dictates what state the game is currently in
# 0: main menu
# 1: escape menu
# 2: placing ships
# 3: player taking turn
# 4: AI taking turn
gameState = 2

clock = pygame.time.Clock()
clock.tick(60)

pygame.display.flip()

# This line creates a 2-dimensional array / matrix. The statement inside the np.array() function that creates 10 dicts
# within each of the 10 lists is courtesy of user Eric on stackoverflow, who is also part of the numpy engineering team
# http://stackoverflow.com/a/13520888
# I could have used the np.matrix() function here to create a strict 2-dimensional array / matrix instead of np.array
# which is able to create n-dimensional arrays. Unfortunately, numpy's matrix data-structure isn't as easy to define
# as an ndarray object. The only advantage that a matrix onject would have over a traditional numpy ndarray object is
# the ability to multiply matrices which I will not be needing to do.
playerMatrix = np.array(
    [[dict([("rect", None), ("hasShip", False), ("isHit", False)]) for d in range(10)] for l in range(10)])
opponentMatrix = np.array(
    [[dict([("rect", None), ("hasShip", False), ("isHit", False)]) for d in range(10)] for l in range(10)])

selectedShip = -1  # when placing ships, this number will correspond to the element of the ship in playerShips which the player has selected
draggingShip = False  # If the player is currently dragging a ship
xDiff = 0  # The difference between the x-coordinate of the mouse and the x-coordinate of the ship rect
yDiff = 0  # The difference between the y-coordinate of the mouse and the y-coordinate of the ship rect
shipRotated = False

placingShip = False
shipReferenceRect = None
allShipsPlaced = False

playerShips = [
    {"size": 5, "rect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 4, "rect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 2, "rect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []}
]

opponentShips = [
    {"size": 5, "rect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 4, "rect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 2, "rect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []}
]


for y in range(0, 10):
    for x in range(0, 10):
        playerMatrix[y][x]["rect"] = pygame.Rect(cellSize[0] * y + 3 * cellSize[0],
                                                 cellSize[1] * x + cellSize[1],
                                                 cellSize[0],
                                                 cellSize[1])
        opponentMatrix[y][x]["rect"] = pygame.Rect(cellSize[0] * y + cellSize[0] * 14,
                                                   cellSize[1] * x + cellSize[1],
                                                   cellSize[0],
                                                   cellSize[1])
        pygame.draw.rect(screen, (128, 128, 128, 255), playerMatrix[y][x]["rect"], 1)
        pygame.draw.rect(screen, (128, 128, 128, 255), opponentMatrix[y][x]["rect"], 1)

opponentMatrix, opponentShips = placeOpponentShips(opponentMatrix, opponentShips)

print(opponentMatrix[3][4]["rect"].center)

pygame.display.update()



while gameLoop:

    mouseX, mouseY = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameLoop = False
        elif ev.type == MOUSEBUTTONDOWN:

            if gameState == 2:

                # I make the element of this loop the position of the dictionary instead of the dictionary itself because I
                # want to reference the dictionary after having found which ship the mouse clicked on
                for ship in range(0, len(playerShips)):

                    rect = playerShips[ship]["rect"]

                    if rect.collidepoint(mouseX, mouseY):

                        selectedShip = ship
                        if playerShips[selectedShip]["shipPlaced"]:
                            playerShips[selectedShip]["shipPlaced"] = False
                            for cell in list(playerShips[selectedShip]["cells"]):
                                playerMatrix[cell[0]][cell[1]]["hasShip"] = False
                            playerShips[selectedShip]["cells"] = []

                        draggingShip = True
                        xDiff = mouseX - rect.x
                        yDiff = mouseY - rect.y

        elif ev.type == MOUSEBUTTONUP:

            if gameState == 2:
                if allShipsPlaced:
                    if confirmShipsButton.rect.collidepoint(mouseX, mouseY):
                        gameState = 3

            if draggingShip:
                draggingShip = False
                placingShip = True

        elif ev.type == KEYDOWN:
            if ev.key == K_r:
                if draggingShip:
                    shipRotated = not shipRotated
                    playerShips[selectedShip]["vertical"] = not playerShips[selectedShip]["vertical"]
                    playerShips[selectedShip]["rect"].height, playerShips[selectedShip]["rect"].width = \
                    playerShips[selectedShip]["rect"].width, playerShips[selectedShip]["rect"].height
                    xDiff, yDiff = yDiff, xDiff

    if draggingShip:
        playerShips[selectedShip]["rect"].x = mouseX - xDiff
        playerShips[selectedShip]["rect"].y = mouseY - yDiff

    screen.blit(background, (0, 0))

    biggestCell = [0]
    if placingShip:
        shipReferenceRect = playerShips[selectedShip]["rect"].copy()
        shipReferenceRect.width, shipReferenceRect.height = cellSize[0], cellSize[1]

    # Iterate through each cell of the matrix row by row
    for y in range(0, 10):
        for x in range(0, 10):

            playerRect = playerMatrix[y][x]["rect"]
            opponentRect = opponentMatrix[y][x]["rect"]

            pygame.draw.rect(screen, (128, 128, 128, 255), playerRect, 10)
            pygame.draw.rect(screen, (128, 128, 128, 255), opponentRect, 10)

            # If the player is placing their ships
            if gameState == 2:
                if placingShip:
                    if playerRect.colliderect(shipReferenceRect):

                        left = max(shipReferenceRect.left, playerRect.left)
                        right = min(shipReferenceRect.right, playerRect.right)
                        bottom = min(shipReferenceRect.bottom, playerRect.bottom)
                        top = max(shipReferenceRect.top, playerRect.top)

                        area = (right - left) * (bottom - top)

                        if area >= biggestCell[0]:
                            biggestCell = [area, x, y]

    if placingShip:
        if len(biggestCell) == 1:
            shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)

        else:
            if playerShips[selectedShip]["vertical"]:
                if playerShips[selectedShip]["size"] + biggestCell[1] > 10:
                    shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)
                else:
                    ableToPlace = True
                    for cell in range(biggestCell[1], biggestCell[1] + playerShips[selectedShip]["size"]):
                        if playerMatrix[cell][biggestCell[2]]["hasShip"]:
                            ableToPlace = False
                    if ableToPlace:
                        shipCell = playerMatrix[biggestCell[2]][biggestCell[1]]["rect"]
                        playerShips[selectedShip]["rect"].x, playerShips[selectedShip][
                            "rect"].y = shipCell.x, shipCell.y
                        for cell in range(biggestCell[1], biggestCell[1] + playerShips[selectedShip]["size"]):
                            playerMatrix[cell][biggestCell[2]]["hasShip"] = True
                            playerShips[selectedShip]["cells"].append((cell, biggestCell[2]))
                        playerShips[selectedShip]["shipPlaced"] = True
                        selectedShip = -1
                    else:
                        shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)

            else:
                if playerShips[selectedShip]["size"] + biggestCell[2] > 10:
                    shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)
                else:
                    ableToPlace = True
                    for cell in range(biggestCell[2], biggestCell[2] + playerShips[selectedShip]["size"]):
                        if playerMatrix[biggestCell[1]][cell]["hasShip"]:
                            ableToPlace = False
                    if ableToPlace:
                        shipCell = playerMatrix[biggestCell[2]][biggestCell[1]]["rect"]
                        playerShips[selectedShip]["rect"].x, playerShips[selectedShip][
                            "rect"].y = shipCell.x, shipCell.y
                        for cell in range(biggestCell[2], biggestCell[2] + playerShips[selectedShip]["size"]):
                            playerMatrix[biggestCell[1]][cell]["hasShip"] = True
                            playerShips[selectedShip]["cells"].append((biggestCell[1], cell))
                        playerShips[selectedShip]["shipPlaced"] = True
                        selectedShip = -1
                    else:
                        shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)

        placingShip = False

    allShipsPlaced = True

    for ship in playerShips:
        pygame.draw.rect(screen, (0, 0, 0, 255), ship["rect"])
        if not ship["shipPlaced"]:
            allShipsPlaced = False

    for ship in opponentShips:
        pygame.draw.rect(screen, (0, 0, 0, 255), ship["rect"])

    if gameState == 2:
        if allShipsPlaced:
            screen.blit(confirmShipsButton.image, confirmShipsButton.rect)

    pygame.display.flip()

pygame.display.quit()
