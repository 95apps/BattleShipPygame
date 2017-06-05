"""
Shayan Khalili
Earl Haig Secondary School, TDSB
shayan.khalili-moghaddam@student.tdsb.on.ca
June 2017

Library of functions and classes for BattleShip game

This includes functions for:

resetShip()
placePlayerShips()
placeOpponentShips()
writeScores()
readScores()

This includes classes for:

Sprite()
MenuButton()
"""

import pygame
from pygame.locals import *
import numpy as np
import random
import os

def resetShip(shipRotated, selectedShip, playerShips):
    # This is a function that, when the player is placing their ships, if the ship is placed in cell that are already
    # occupied by a ship, will return the ship to its starting position outside of the board
    # INPUT AND OUTPUT:
    #   shipRotated - bool: bool that dictates whether the currently selected ship is vertical or horizontal, not
    #   necessary anymore since the playerShips dictionaries have the ["vertical"] bool but still implemented for sake
    #   of ease
    #   selectedShip - int: integer from 0 to 4 to dictate which ship is currently selected by the player in the
    #   playerShips dictionary
    #   playerShips - list of dicts: a list with 5 elements for the 5 ships. Each element is a dictionary that includes
    #   the necessary values for the ships, such as their size, the cells they occupy, etc...

    # if the ship is horizontal, make it vertical
    if shipRotated:
        shipRotated = False
        playerShips[selectedShip]["vertical"] = True
        playerShips[selectedShip]["surface"] = pygame.transform.rotate(playerShips[selectedShip]["surface"], 90)

    # return the ship's rect object to its starting position and dimensions
    playerShips[selectedShip]["rect"] = playerShips[selectedShip]["startingRect"].copy()
    selectedShip = -1

    return shipRotated, selectedShip, playerShips



def placePlayerShips(playerMatrix, playerShips, selectedShip, biggestCell, shipRotated):
    # This function will place or reset a ship that has been released after being dragged by the player
    # INPUT:
    #   playerMatrix - matrix (lists inside list): matrix that maps the cells on the player's board, needed to assign
    #   values to the cells that the ship will occupy
    #   playerShips - list of dicts: a list with 5 elements for the 5 ships. Each element is a dictionary that includes
    #   the necessary values for the ships, such as their size, the cells they occupy, etc...
    #   selectedShip - int: the ship currently being placed
    #   biggestCell - list: the area and x and y positions within the playerMatrix of the cell that had the greatest
    #   area of intersection with the top left square of the ship
    #   shipRotated - bool: dictates whether the currently selected ship is vertical or horizontal
    # OUTPUT:
    #   playerMatrix - matrix (lists inside list): matrix that maps the cells on the player's board, with the newly
    #   placed ship assigned to the cells
    #   playerShips - list of dicts: a list with 5 elements for the 5 ships. Each element is a dictionary that includes
    #   the necessary values for the ships, such as their size, the cells they occupy, etc...
    #   selectedShip - int: the ship currently being placed, will always return as -1

    # if the ship was not placed on the board, reset ship
    if len(biggestCell) == 1:
        shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)

    else:
        if playerShips[selectedShip]["vertical"]:  # if the ship is vertical
            if playerShips[selectedShip]["size"] + biggestCell[2] > 10:  # if placing the ship will exceed the bounds of the board, reset the ship
                shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)
            else:
                # check if the cells that the ship will occupy are already occupied by any ships
                ableToPlace = True
                for cell in range(biggestCell[2], biggestCell[2] + playerShips[selectedShip]["size"]):
                    if playerMatrix[cell][biggestCell[1]]["hasShip"]:
                        ableToPlace = False

                # if none of the cells are already occupied, place the ship
                if ableToPlace:
                    # reference to the biggestCell rect object for ease of use and readability
                    shipCell = playerMatrix[biggestCell[2]][biggestCell[1]]["rect"]
                    # position the rect object of the ship to the biggestCell rect object's position
                    playerShips[selectedShip]["rect"].x, playerShips[selectedShip]["rect"].y = shipCell.x, shipCell.y
                    # iterate through the cells that the ship will occupy and set their "hasShip" value to true
                    for cell in range(biggestCell[2], biggestCell[2] + playerShips[selectedShip]["size"]):
                        playerMatrix[cell][biggestCell[1]]["hasShip"] = True
                        playerShips[selectedShip]["cells"].append((cell, biggestCell[1]))
                    # set the "shipPlaced" value of the ship being placed to True
                    playerShips[selectedShip]["shipPlaced"] = True
                    selectedShip = -1
                else:
                    shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)

        else:
            if playerShips[selectedShip]["size"] + biggestCell[1] > 10:  # if placing the ship will exceed the bounds of the board, reset the ship
                shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)
            else:
                # check if the cells that the ship will occupy are already occupied by any ships
                ableToPlace = True
                for cell in range(biggestCell[1], biggestCell[1] + playerShips[selectedShip]["size"]):
                    if playerMatrix[biggestCell[2]][cell]["hasShip"]:
                        ableToPlace = False

                # if none of the cells are already occupied, place ship
                if ableToPlace:
                    # reference to the biggestCell rect object for ease of use and readability
                    shipCell = playerMatrix[biggestCell[2]][biggestCell[1]]["rect"]
                    # position the rect object of the ship to the biggestCell rect object's position
                    playerShips[selectedShip]["rect"].x, playerShips[selectedShip]["rect"].y = shipCell.x, shipCell.y
                    # iterate through the cells that the ship will occupy and set their "hasShip" value to true
                    for cell in range(biggestCell[1], biggestCell[1] + playerShips[selectedShip]["size"]):
                        playerMatrix[biggestCell[2]][cell]["hasShip"] = True
                        playerShips[selectedShip]["cells"].append((biggestCell[2], cell))
                    # set the "shipPlaced" value of the ship being placed to True
                    playerShips[selectedShip]["shipPlaced"] = True
                    selectedShip = -1
                else:
                    shipRotated, selectedShip, playerShips = resetShip(shipRotated, selectedShip, playerShips)

    return playerMatrix, playerShips, selectedShip



def placeOpponentShips(opponentMatrix, opponentShips):
    # This function will position the opponent's ships on its board randomly
    # INPUT AND OUTPUT:
    #   opponentMatrix - matrix (lists inside list): matrix that maps the cells on the opponent's board, needed to assign
    #   values to the cells that the ship will occupy
    #   opponentShips - list of dicts: a list with 5 elements for the 5 ships. Each element is a dictionary that includes
    #   the necessary values for the ships, such as their size, the cells they occupy, etc...

    # iterate through each of the 5 ships
    for ship in range(0, 5):

        shipPlaced = False  # control variable for while loop
        while not shipPlaced:  # while ship has not been placed

            orientation = random.randint(0, 1)  # randomly orient the ship horizontally or vertically

            if orientation == 0:  # if orientation is 0 (vertical)
                # randomly select a cell for the top left square of the ship to be placed in
                biggestCell = [0, random.randint(0, 9), random.randint(0, 9)]
                opponentShips[ship]["vertical"] = True

                # if ship will not go out of the boards bounds
                if not opponentShips[ship]["size"] + biggestCell[2] > 10:
                    # check if the cells that the ship will occupy are already occupied by any ships
                    ableToPlace = True
                    for cell in range(biggestCell[2], biggestCell[2] + opponentShips[ship]["size"]):
                        if opponentMatrix[cell][biggestCell[1]]["hasShip"]:
                            ableToPlace = False

                    # if none of the cells are already occupied, place ship
                    if ableToPlace:
                        # reference to the biggestCell rect object for ease of use and readability
                        shipCell = opponentMatrix[biggestCell[2]][biggestCell[1]]["rect"]
                        # position the rect object of the ship to the biggestCell rect object's position
                        opponentShips[ship]["rect"].x, opponentShips[ship]["rect"].y = shipCell.x, shipCell.y
                        # iterate through the cells that the ship will occupy and set their "hasShip" value to true
                        for cell in range(biggestCell[2], biggestCell[2] + opponentShips[ship]["size"]):
                            opponentMatrix[cell][biggestCell[1]]["hasShip"] = True
                            opponentShips[ship]["cells"].append((cell, biggestCell[1]))
                        # set the "shipPlaced" value of the ship being placed to True
                        opponentShips[ship]["shipPlaced"] = True
                        shipPlaced = True

            else:  # else if orientation is 1 (horizontal)
                # randomly select a cell for the top left square of the ship to be placed in
                biggestCell = [0, random.randint(0, 9), random.randint(0, 9)]
                opponentShips[ship]["vertical"] = False

                # if ship will not go out of the boards bounds
                if not opponentShips[ship]["size"] + biggestCell[1] > 10:
                    # check if the cells that the ship will occupy are already occupied by any ships
                    ableToPlace = True
                    for cell in range(biggestCell[1], biggestCell[1] + opponentShips[ship]["size"]):
                        if opponentMatrix[biggestCell[2]][cell]["hasShip"]:
                            ableToPlace = False

                    # if none of the cells are already occupied, place ship
                    if ableToPlace:
                        # rotate the rect and surface objects of the ship horizontally
                        opponentShips[ship]["rect"].width, opponentShips[ship]["rect"].height = opponentShips[ship]["rect"].height, opponentShips[ship]["rect"].width
                        opponentShips[ship]["surface"] = pygame.transform.rotate(opponentShips[ship]["surface"], 90)
                        # reference to the biggestCell rect object for ease of use and readability
                        shipCell = opponentMatrix[biggestCell[2]][biggestCell[1]]["rect"]
                        # position the rect object of the ship to the biggestCell rect object's position
                        opponentShips[ship]["rect"].x, opponentShips[ship]["rect"].y = shipCell.x, shipCell.y
                        # iterate through the cells that the ship will occupy and set their "hasShip" value to true
                        for cell in range(biggestCell[1], biggestCell[1] + opponentShips[ship]["size"]):
                            opponentMatrix[biggestCell[2]][cell]["hasShip"] = True
                            opponentShips[ship]["cells"].append((biggestCell[2], cell))
                        # set the "shipPlaced" value of the ship being placed to True
                        opponentShips[ship]["shipPlaced"] = True
                        shipPlaced = True

    return opponentMatrix, opponentShips

def writeScore(winner, moves):
    # A function that will write the winner and their number of moves to the scores.csv file when either the player or
    # the opponent wins
    # INPUT:
    #   winner - string: a string that can either be "player" or "opponent" representing the winner of the game
    #   moves - int: the number of moves made by the winner during the game
    # OUTPUT:
    #   scores.csv - csv file: A csv file with the two columns of winner and # of moves, each row representing a game

    with open("scores.csv", "a+") as f:
        # write the winner in the first column and the number of moves in the second column
        f.write(winner + "," + str(moves) + "\n")

def readScores():
    # A function that will read the scores.csv file in order to display the most recent scores to the player
    # OUTPUT:
    #   scoreList - list of tuples: stores the winner and number of moves they took of the recent games

    scoreList = []  # list of tuples that holds scores

    if "scores.csv" in os.listdir():
        with open("scores.csv") as f:
            for line in f:
                # split the line into a list delimited by a comma, and ignoring the \n character
                lineList = line[:-1].split(",")
                # appent a tuple of (winner, moves) to the scoreList
                scoreList.append((lineList[0], lineList[1]))

        # reverse the list to show most recent scores first
        scoreList.reverse()

    return scoreList

class Sprite(pygame.sprite.Sprite):
    # this class is used to resize images and create a rect for the image to match the game's grid system

    def __init__(self, path, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path)  # load the image as a surface
        self.image = pygame.transform.scale(self.image, (width, height))  # resize image to grid
        self.image = self.image.convert_alpha()  # convert while keeping transparency
        self.rect = pygame.Rect(x, y, width, height)  # create rect object to match image

class MenuButton(pygame.sprite.Sprite):
    # this class is used specifically for menu buttons which need to be identified by a name

    def __init__(self, name, path, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = Sprite(path, x, y, width, height)  # create and resize the image and rect objects
        self.name = name  # assign the name variable
