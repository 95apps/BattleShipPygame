"""
PSEUDOCODE:

while game loop:
    if close button pressed:
        close game
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

gameLoop = True

clock = pygame.time.Clock()
clock.tick(30)

pygame.display.flip()

# This line creates a 2-dimensional array / matrix. The statement inside the np.array() function that creates 10 dicts
# within each of the 10 lists is courtesy of user Eric on stackoverflow, who is also part of the numpy engineering team
# http://stackoverflow.com/a/13520888
# I could have used the np.matrix() function here to create a strict 2-dimensional array / matrix instead of np.array
# which is able to create n-dimensional arrays. Unfortunately, numpy's matrix data-structure isn't as easy to define
# as an ndarray object. The only advantage that a matrix onject would have over a traditional numpy ndarray object is
# the ability to multiply matrices which I will not be needing to do.
playerMatrix = np.array([[dict() for d in range(10)] for l in range(10)])
opponentMatrix = np.array([[dict() for d in range(10)] for l in range(10)])

selectedShip = -1

playerShips = [
    {"size": 5, "rect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5), "hit": 0},
    {"size": 4, "rect": Rect(cellSize[0] * 0, cellSize[1] * 6, cellSize[0], cellSize[1] * 4), "hit": 0},
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
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameLoop = False

    screen.blit(background, (0, 0))

    for y in range (0, 10):
        for x in range (0, 10):
            pygame.draw.rect(screen, (128, 128, 128, 255), playerMatrix[x][y]["rect"], 10)
            pygame.draw.rect(screen, (128, 128, 128, 255), opponentMatrix[x][y]["rect"], 10)

    pygame.display.update()


pygame.display.quit()
