"""
Shayan Khalili
May 22, 2017
Submitted to Mr. Cope, ICS3U1 - 03

BattleshipV8.py
The game battleship played by the user against the computer
Input: mouse clicks and keystrokes
Output: pygame window displaying the game and a csv file storing the scores of the recent games
"""

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
            if in main menu:
                if player click new game:
                    proceed to game
                if player click rules:
                    show rules
                if player click scores:
                    show scores
            if in escape menu:
                if player click resume:
                    resume game
                if player click rules:
                    show rules
                if player click scores:
                    show scores
            if dragging ship:
                if ship on board:
                    place ship on board
                else:
                    return ship to start
            if player taking turn:
                if player clicks on opponent board:
                    if the cell has a ship:
                        place red marker and assign appropriate values
                        if player has destroyer all opponent ships:
                            player wins
                            record score in csv
                    else:
                        place white marker and assign appropriate values
            if opponent taking turn:
                select random cell on player board:
                    if cell has a ship:
                        place red marker and assign appropriate values
                        if opponent has destroyer all player ships:
                            opponent wins
                            record score in csv
                    else:
                        place white marker and assign appropriate values
        if game state is on main menu:
            blit main menu

    if all ships have been placed:
        change game state to start game

    blit background image
    blit boards
"""

import pygame
from pygame.locals import *
import numpy as np
from BattleShipLibrary import *

# initiate pygame and the mixer
pygame.mixer.pre_init(44100, -16, 2, 1024)  # frequency, size, channels, buffersize
pygame.init()

# Get the resolution of the screen to make the game the same size
screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h - 50)

# Size of each cell
cellSize = (int(screenSize[0]) / 24, int(screenSize[0] / 24))

# Size of each board
boardSize = (cellSize[0] * 10, cellSize[1] * 10)

# Setting up the screen
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("BATTLESHIP")

# Ocean background
background = pygame.image.load("resources/images/TopDownOcean.jpg")
background = background.convert()

confirmShipsButton = Sprite("resources/images/ConfirmShipsButton.png", cellSize[0] * 6, cellSize[1] * 12, int(cellSize[0]) * 4, int(cellSize[1]))
menu = Sprite("resources/images/MainMenu.png", cellSize[0] * 9, 0, int(cellSize[0]) * 8, int(cellSize[1]) * 16)
rulesDisplay = Sprite("resources/images/RulesDisplay.png", cellSize[0] * 9, 0, int(cellSize[0]) * 8, int(cellSize[1]) * 16)
mainMenuButtons = [MenuButton("newgame", "resources/images/NewGameButton.png", cellSize[0] * 9, cellSize[1] * 3, int(cellSize[0] * 8), int(cellSize[1] * 2)),
                   MenuButton("rules", "resources/images/RulesButton.png", cellSize[0] * 9, cellSize[1] * 6, int(cellSize[0] * 8), int(cellSize[1] * 2)),
                   MenuButton("scores", "resources/images/ScoresButton.png", cellSize[0] * 9, cellSize[1] * 9, int(cellSize[0] * 8), int(cellSize[1] * 2))]
escapeMenuButtons = [MenuButton("resume", "resources/images/ResumeButton.png", cellSize[0] * 9, cellSize[1] * 3, int(cellSize[0] * 8), int(cellSize[1] * 2)),
                   MenuButton("rules", "resources/images/RulesButton.png", cellSize[0] * 9, cellSize[1] * 6, int(cellSize[0] * 8), int(cellSize[1] * 2)),
                   MenuButton("scores", "resources/images/ScoresButton.png", cellSize[0] * 9, cellSize[1] * 9, int(cellSize[0] * 8), int(cellSize[1] * 2))]



# gameState dictates what state the game is currently in
# 0: main menu
# 1: escape menu
# 2: placing ships
# 3: player taking turn
# 4: AI taking turn
# 5: player won
# 6: AI won
# 7: displaying rules
# 8: displaying recent scores
gameState = 0

# this variable will be used to return to the last game state after the player has for example opened a menu
lastGameState = 0

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
shipRotated = False  # If the selected ship is rotated vertically (False) or horizontally (True)

placingShip = False  # Bool dictating whether in the current frame the ship is being placed on the board or not

# Used as a copy of the Rect object of the ship currently being dragged/placed in order to manipulate and test whether
# the ship can be placed without modifying the original Rect object of the ship
shipReferenceRect = None
# Bool dictating whether all the ships have been placed, only used for making
# "Confirm Placement" button appear and disappear since usually gameState will be used to dictate what state the game is in
allShipsPlaced = False

mouseUp = False
targetingCell = False  # Bool dictating whether in the current fram the player is targeting one of the opponent's cells or not
targetedCell = None  # Holds the coordinates of the cell in the opponent's matrix which the player has targeted

playerHitCount = 0  # Number of times the player has hit the opponent's ships
opponentHitCount = 0  # Number of times the opponent has hit the player's ships

# sound effects
clickSound = pygame.mixer.Sound(file="resources/sounds/click.ogg")
explosionSound = pygame.mixer.Sound(file="resources/sounds/explosion.ogg")
hitSound = pygame.mixer.Sound(file="resources/sounds/hitSound.ogg")
missSound = pygame.mixer.Sound(file="resources/sounds/missSound.ogg")

# load one of two songs randomly
pygame.mixer.music.load(["resources/music/CrossingTheChasm.ogg", "resources/music/Hitman.ogg"][random.randint(0, 1)])
pygame.mixer.music.set_volume(0.4)  # set volume of music
pygame.mixer.music.play(-1)  # play music and loop infinitely

gameFont = pygame.font.SysFont("impact", 30)  # Font object to be used for creating text in the game
yourBoardText = gameFont.render("YOUR BOARD", True, (0, 0, 0))
opponentBoardText = gameFont.render("OPPONENT BOARD", True, (0, 0, 0))
pressRText = gameFont.render("PRESS \"R\" TO ROTATE SHIP", True, (0, 0, 0))
pressEscapeText = gameFont.render("PRESS ESCAPE FOR MENU", True, (0, 0, 0))
youWonText = gameFont.render("YOU WON!", True, (0, 0, 0))
opponentWonText = gameFont.render("OPPONENT WON :(", True, (0, 0, 0))

playerMoves = 0  # the number of moves the player has made
opponentMoves = 0  # the number of moves the opponent has made

# The list that the recent games' scores will be held in
scoreList = None

# The list of the player's ships
playerShips = [
    {"size": 5, "rect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size5.png")), (int(cellSize[0]), int(cellSize[1]) * 5)),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 4, "rect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size4.png")), (int(cellSize[0]), int(cellSize[1]) * 4)),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size3a.png")), (int(cellSize[0]), int(cellSize[1]) * 3)),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size3b.png")), (int(cellSize[0]), int(cellSize[1]) * 3)),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 2, "rect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size2.png")), (int(cellSize[0]), int(cellSize[1]) * 2)),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []}
]

# list of the opponent's ships
opponentShips = [
    {"size": 5, "rect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size5.png")), (int(cellSize[0]), int(cellSize[1]) * 5)),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1], cellSize[0], cellSize[1] * 5),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 4, "rect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size4.png")), (int(cellSize[0]), int(cellSize[1]) * 4)),
     "startingRect": Rect(cellSize[0] * 0, cellSize[1] * 7, cellSize[0], cellSize[1] * 4),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size3a.png")), (int(cellSize[0]), int(cellSize[1]) * 3)),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1], cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 3, "rect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size3b.png")), (int(cellSize[0]), int(cellSize[1]) * 3)),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 5, cellSize[0], cellSize[1] * 3),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []},
    {"size": 2, "rect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "surface":pygame.transform.scale((pygame.image.load("resources/images/size2.png")), (int(cellSize[0]), int(cellSize[1]) * 2)),
     "startingRect": Rect(cellSize[0] * 2, cellSize[1] * 9, cellSize[0], cellSize[1] * 2),
     "hit": 0, "vertical": True, "shipPlaced": False, "cells": []}
]

# This list will store the player's matrix but in a 1-dimensional list and only the positions of the cells within the
# matrix, in order for the computer to be able to randomly select one of the players cells when its taking its turn,
# and not repeat cells.
opponentTargets = []

# This loop will position all of the player and opponent's boards cells properly, and draw them on the screen for the first time
for y in range(0, 10):
    for x in range(0, 10):
        opponentTargets.append((y, x))
        playerMatrix[y][x]["rect"] = pygame.Rect(cellSize[0] * x + cellSize[0] * 3,
                                                 cellSize[1] * y + cellSize[1],
                                                 cellSize[0],
                                                 cellSize[1])
        opponentMatrix[y][x]["rect"] = pygame.Rect(cellSize[0] * x + cellSize[0] * 14,
                                                   cellSize[1] * y + cellSize[1],
                                                   cellSize[0],
                                                   cellSize[1])
        pygame.draw.rect(screen, (128, 128, 128, 255), playerMatrix[y][x]["rect"], 1)
        pygame.draw.rect(screen, (128, 128, 128, 255), opponentMatrix[y][x]["rect"], 1)

# run function to automatically place the computer's ships
opponentMatrix, opponentShips = placeOpponentShips(opponentMatrix, opponentShips)

pygame.display.update()

gameLoop = True

while gameLoop:

    mouseUp = False
    mouseX, mouseY = pygame.mouse.get_pos()
    targetingCell = False

    """
    EVENTS
    """

    # iterate through the events in the current frame
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            gameLoop = False

        elif ev.type == MOUSEBUTTONDOWN:

            clickSound.play()

            # if placing ships
            if gameState == 2:

                # iterate through each ship in the list of playerShips
                # I make the element of this loop the position of the dictionary instead of the dictionary itself because I
                # want to reference the dictionary after having found which ship the mouse clicked on
                for ship in range(0, len(playerShips)):

                    # create variable referencing the rect object of the ship for sake of simplicity and readability
                    rect = playerShips[ship]["rect"]

                    # if the cursor position is on the ship
                    if rect.collidepoint(mouseX, mouseY):

                        selectedShip = ship  # the selected ship variable is assigned to the current ship to be dragged
                        # if the ship was already on the board, iterate through the cells that the ship was previously
                        # occupying and set their "hasShip" value to False. Also set the "cells" value of the current
                        # ship to an empty list, and the "shipPlaced" value to False
                        if playerShips[selectedShip]["shipPlaced"]:
                            playerShips[selectedShip]["shipPlaced"] = False
                            for cell in list(playerShips[selectedShip]["cells"]):
                                playerMatrix[cell[0]][cell[1]]["hasShip"] = False
                            playerShips[selectedShip]["cells"] = []

                        draggingShip = True

                        # These difference variables will essentially change the pivot point of the ship being moved to
                        # the coordinates of the mouse for aesthetic reasons
                        xDiff = mouseX - rect.x
                        yDiff = mouseY - rect.y

        elif ev.type == MOUSEBUTTONUP:

            clickSound.play()

            mouseUp = True

            # if in main menu, check which button was clicked and act accordingly
            if gameState == 0:
                for button in mainMenuButtons:
                    if button.sprite.rect.collidepoint(mouseX, mouseY):
                        if button.name == "newgame":
                            gameState = 2
                        elif button.name == "rules":
                            lastGameState = gameState
                            gameState = 7
                        elif button.name == "scores":
                            lastGameState = gameState
                            gameState = 8
                            scoreList = readScores()

            # if in escape menu, check which button was clicked and act accordingly
            elif gameState == 1:
                for button in escapeMenuButtons:
                    if button.sprite.rect.collidepoint(mouseX, mouseY):
                        if button.name == "resume":
                            gameState = lastGameState
                        elif button.name == "rules":
                            gameState = 7
                        elif button.name == "scores":
                            gameState = 8
                            scoreList = readScores()

            # if all ships have been placed and the "confirm placement" button has been pressed, start game
            elif gameState == 2 and allShipsPlaced and confirmShipsButton.rect.collidepoint(mouseX, mouseY):
                gameState = 3

            # if left click while displaying rules, go to last game state
            elif gameState == 7:
                gameState = lastGameState
            # if left click while displaying scores, go to last game state
            elif gameState == 8:
                gameState = lastGameState

            # if player was dragging ship, stop dragging and begin placing ship procedure
            if draggingShip:
                draggingShip = False
                placingShip = True

        elif ev.type == KEYDOWN:

            # if "R" is pressed while dragging a ship, rotate the ship's surface and rect object
            if ev.key == K_r and draggingShip:
                shipRotated = not shipRotated
                playerShips[selectedShip]["vertical"] = not playerShips[selectedShip]["vertical"]
                playerShips[selectedShip]["rect"].height, playerShips[selectedShip]["rect"].width = playerShips[selectedShip]["rect"].width, playerShips[selectedShip]["rect"].height
                playerShips[selectedShip]["surface"] = pygame.transform.rotate(playerShips[selectedShip]["surface"], 90)
                xDiff, yDiff = yDiff, xDiff

            # if escape is pressed and the game is not in a menu/rules/scores, go to escape menu
            if ev.key == K_ESCAPE and gameState not in(0, 1, 7, 8):
                lastGameState = gameState
                gameState = 1


    """
    PROCESSING
    """

    # blit background and permanent text
    screen.blit(background, (0, 0))
    screen.blit(yourBoardText, (cellSize[0] * 3, 0))
    screen.blit(opponentBoardText, (cellSize[0] * 14, 0))
    screen.blit(pressEscapeText, (cellSize[0] * 18, 0))

    # if a ship is being dragged, make its x and y coordinates equal to the mouse - the differences when it was picked up
    if draggingShip:
        screen.blit(pressRText, (cellSize[0] * 8, 0))
        playerShips[selectedShip]["rect"].x = mouseX - xDiff
        playerShips[selectedShip]["rect"].y = mouseY - yDiff

    biggestCell = [0]  # this is the variable that will dictate which cell the top left corner of the ship should be placed in

    if placingShip:
        shipReferenceRect = playerShips[selectedShip]["rect"].copy()
        # the size of the reference rectangle is made to a square of cellSize in order to determine which of the cells that the top left of the ship collides with have
        # the biggest area, in order to determine which cell the top left of the ship should go in
        shipReferenceRect.width, shipReferenceRect.height = cellSize[0], cellSize[1]

    # Iterate through each cell of the matrix row by row
    for y in range(0, 10):
        for x in range(0, 10):

            playerRect = playerMatrix[y][x]["rect"].copy()
            opponentRect = opponentMatrix[y][x]["rect"].copy()

            pygame.draw.rect(screen, (128, 128, 128, 255), playerRect, 10)
            pygame.draw.rect(screen, (128, 128, 128, 255), opponentRect, 10)

            # If the player is placing their ships
            if gameState == 2:
                if placingShip:
                    if playerRect.colliderect(shipReferenceRect):

                        # determine length of sides of intersection area between top left square of ship and the current cell
                        left = max(shipReferenceRect.left, playerRect.left)
                        right = min(shipReferenceRect.right, playerRect.right)
                        bottom = min(shipReferenceRect.bottom, playerRect.bottom)
                        top = max(shipReferenceRect.top, playerRect.top)

                        # determine area of intersection between top left square of ship and the current cell
                        area = (right - left) * (bottom - top)

                        # if the area is greater than the previously recorded area, this is the bigger cell, therefore
                        # the ship's top left square should go in this cell, and the rest of the ship should be placed accordingly
                        if area >= biggestCell[0]:
                            biggestCell = [area, x, y]

            # if player taking turn and mouse has been released
            elif gameState == 3 and mouseUp:

                # if the current cell on the opponent's board collides with the mouse position
                if opponentRect.collidepoint((mouseX, mouseY)) and not opponentMatrix[y][x]["isHit"]:
                    playerMoves += 1  # increment the number of moves the player has made
                    opponentMatrix[y][x]["isHit"] = True
                    if opponentMatrix[y][x]["hasShip"]:
                        hitSound.play()
                    else:
                        missSound.play()

                    targetingCell = True  # in the current frame, a cell is being targeted

                    # the cell that is targeted by the player, if a player hit a ship, this is used to check which ship
                    # was hit
                    targetedCell = (y, x)

            # blit the white markers on the player's board
            if playerMatrix[y][x]["isHit"] and not playerMatrix[y][x]["hasShip"]:
                    pygame.draw.circle(screen, (255, 255, 255, 255), playerRect.center, int(cellSize[0] / 2.5))

            # blit the white markers on the opponent's board
            if opponentMatrix[y][x]["isHit"] and not opponentMatrix[y][x]["hasShip"]:
                    pygame.draw.circle(screen, (255, 255, 255, 255), opponentRect.center, int(cellSize[0] / 2.5))


    if placingShip:

        # place ship
        playerMatrix, playerShips, selectedShip = placePlayerShips(playerMatrix, playerShips, selectedShip, biggestCell, shipRotated)

        # reset variables for next use
        shipRotated = False
        placingShip = False


    opponentTargetedCell = None  # this variable will store the x and y coordinates of the cell that the opponent will target within the player's matrix

    if gameState == 4:
        cellIndex = random.randint(0, len(opponentTargets) - 1)
        opponentTargetedCell = opponentTargets.pop(cellIndex)
        playerMatrix[opponentTargetedCell[0]][opponentTargetedCell[1]]["isHit"] = True
        opponentMoves += 1  # increment the number of moves the opponent has made

    allShipsPlaced = True

    # for each of the player's ships
    for ship in playerShips:

        # blit the player's ship onto the screen
        screen.blit(ship["surface"], ship["rect"])

        # if placing ships and not all ships have been placed, allShipsPlaced = False
        if gameState == 2:
            if not ship["shipPlaced"]:
                allShipsPlaced = False

        # if AI taking turn
        elif gameState == 4:
            # if the targeted cell is one of the cells the ship is occupying
            if opponentTargetedCell in ship["cells"]:
                # increment the ship's hit counter, and the opponent's hit counter
                ship["hit"] += 1  # increment "hit" value of ship by 1
                if ship["hit"] >= ship["size"]:  # if ship has been destroyed, play explosion sound
                    explosionSound.play()
                opponentHitCount += 1

                # If the opponent has 17 hits on ships, the opponent wins
                if opponentHitCount >= 17:
                    writeScore("opponent", opponentMoves)
                    gameState = 6
                    print("opponent has won :(")

        # for each cell that the ship is occupying
        for cell in ship["cells"]:
            # if the cell has been hit
            if playerMatrix[cell[0]][cell[1]]["isHit"]:
                # draw a red marker on the cell
                pygame.draw.circle(screen, (255, 0, 0, 255), playerMatrix[cell[0]][cell[1]]["rect"].center, int(cellSize[0] / 2.5))

    # for each of the opponent's ships
    for ship in opponentShips:

        # if the ship has been destroyed, blit the ship on the screen
        if ship["hit"] >= ship["size"]:
            screen.blit(ship["surface"], ship["rect"])

        # if player has taken turn
        if gameState == 3 and targetingCell:
            # if the cell targeted by the player is one of the cells that the ship is occupying
            if targetedCell in ship["cells"]:
                ship["hit"] += 1  # increment "hit" value of ship by 1
                if ship["hit"] >= ship["size"]:  # if ship has been destroyed, play explosion sound
                    explosionSound.play()
                playerHitCount += 1

                # If the player has 17 hits on ships, the player wins
                if playerHitCount >= 17:
                    writeScore("player", playerMoves)
                    gameState = 5
                    print("you have won :)")

        # for each cell that the ship is occupying
        for cell in ship["cells"]:
            # if the cell has been hit
            if opponentMatrix[cell[0]][cell[1]]["isHit"]:
                # draw a red marker on the cell
                pygame.draw.circle(screen, (255, 0, 0, 255), opponentMatrix[cell[0]][cell[1]]["rect"].center, int(cellSize[0] / 2.5))

    """
    GAME STATE HANDLING
    """

    if gameState == 0:  # if in main menu, blit menu and buttons
        screen.blit(menu.image, menu.rect)
        for button in mainMenuButtons:
            screen.blit(button.sprite.image, button.sprite.rect)
    elif gameState == 1:  # if in escape menu, blit menu and buttons
        screen.blit(menu.image, menu.rect)
        for button in escapeMenuButtons:
            screen.blit(button.sprite.image, button.sprite.rect)
    elif gameState == 2 and allShipsPlaced:  # if all ships have been placed but not confirmed, show confirm ships button
        screen.blit(confirmShipsButton.image, confirmShipsButton.rect)
    elif gameState == 3 and targetingCell:  # if player has taken their turn, go to opponent turn
        gameState = 4
    elif gameState == 4:  # if opponent has taken its turn, go to player turn
        gameState = 3
    elif gameState == 5:  # if player has won, blit corresponding text
        screen.blit(youWonText, (cellSize[0] * 8, 0))
    elif gameState == 6:  # if opponent has won, blit corresponding text
        screen.blit(opponentWonText, (cellSize[0] * 8, 0))
    elif gameState == 7:  # if showing rules, blit rules page
        screen.blit(rulesDisplay.image, rulesDisplay.rect)
    elif gameState == 8:  # if showing scores, blit scores
        screen.blit(menu.image, menu.rect)
        # blit the chart header
        screen.blit(gameFont.render("Game # (new to old) | Winner | # of Moves", True, (200, 0, 0)), (cellSize[0] * 9 + 20, cellSize[1] * 2))
        # If scoreList is not empty
        if len(scoreList) > 0:
            # blit each score until the 8th most recent game, or the oldest game if there are less than 8 games
            for score in range(0, min(len(scoreList), 8)):
                screen.blit(gameFont.render(str(score) + " | " + scoreList[score][0] + " | " + scoreList[score][1], True, (0, 0, 0)), (cellSize[0] * 9 + 20, cellSize[1] * (3 + score)))

    pygame.display.flip()

pygame.display.quit()
