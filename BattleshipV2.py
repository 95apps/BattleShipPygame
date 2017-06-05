"""
PSEUDOCODE:

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
                put ship back to start

    blit background image
    blit boards
"""

import pygame
from pygame.locals import *
import numpy as np

pygame.init()

screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)

cellSize = (int(screenSize[0]) / 24, int(screenSize[0] / 24))

boardSize = (cellSize[0] * 10, cellSize[1] * 10)

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("BATTLESHIP")

background = pygame.image.load("resources/TopDownOcean.jpg")
background = background.convert()

gameLoop = True

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
playerMatrix = np.array([[dict([("rect", None), ("hasShip", False), ("isHit", False)]) for d in range(10)] for l in range(10)])
opponentMatrix = np.array([[dict([("rect", None), ("hasShip", False), ("isHit", False)]) for d in range(10)] for l in range(10)])

selectedShip = -1
draggingShip = False
xDiff = 0
yDiff = 0
startingRect = None
shipRotated = False

playerShips = [
    {"size": 5, "rect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5), "hit": 0},
    {"size": 4, "rect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4), "hit": 0},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3), "hit": 0},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3), "hit": 0},
    {"size": 2, "rect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2), "hit": 0}
]

for y in range (0, 10):
    for x in range (0, 10):
        playerMatrix[x][y]["rect"] = pygame.Rect(cellSize[0] * x + 3 * cellSize[0],
                                                 cellSize[1] * y + cellSize[1],
                                                 cellSize[0],
                                                 cellSize[1])
        opponentMatrix[x][y]["rect"] = pygame.Rect(cellSize[0] * x + cellSize[0] * 14,
                                                   cellSize[1] * y + cellSize[1],
                                                   cellSize[0],
                                                   cellSize[1])
        pygame.draw.rect(screen, (128, 128, 128, 255), playerMatrix[x][y]["rect"], 1)
        pygame.draw.rect(screen, (128, 128, 128, 255), opponentMatrix[x][y]["rect"], 1)

pygame.display.update()



while gameLoop:

    x, y = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameLoop = False
        elif ev.type == MOUSEBUTTONDOWN:


            # I make the element of this loop the position of the dictionary instead of the dictionary itself because I
            # want to reference the dictionary after having found which ship the mouse clicked on
            for ship in range(0, len(playerShips)):

                rect = playerShips[ship]["rect"]

                if rect.collidepoint(x, y):

                    selectedShip = ship
                    draggingShip = True
                    xDiff = x - rect.x
                    yDiff = y - rect.y
                    startingRect = rect.copy()

        elif ev.type == MOUSEBUTTONUP:
            if draggingShip:


                if shipRotated:
                    playerShips[selectedShip]["rect"].height, playerShips[selectedShip]["rect"].width = playerShips[selectedShip]["rect"].width, playerShips[selectedShip]["rect"].height
                    shipRotated = False

                draggingShip = False
                playerShips[selectedShip]["rect"] = startingRect.copy()
                selectedShip = -1
                startingRect = None

        elif ev.type == KEYDOWN:
            if ev.key == K_r:
                if draggingShip:
                    shipRotated = not shipRotated
                    playerShips[selectedShip]["rect"].height, playerShips[selectedShip]["rect"].width = playerShips[selectedShip]["rect"].width, playerShips[selectedShip]["rect"].height
                    xDiff, yDiff = yDiff, xDiff


    if draggingShip:
        playerShips[selectedShip]["rect"].x = x - xDiff
        playerShips[selectedShip]["rect"].y = y - yDiff

    screen.blit(background, (0, 0))

    for y in range (0, 10):
        for x in range (0, 10):
            pygame.draw.rect(screen, (128, 128, 128, 255), playerMatrix[x][y]["rect"], 10)
            pygame.draw.rect(screen, (128, 128, 128, 255), opponentMatrix[x][y]["rect"], 10)

    for ship in playerShips:
        pygame.draw.rect(screen, (0, 0, 0, 255), ship["rect"])

    pygame.display.flip()


pygame.display.quit()
