"""
Testing out Fonts
"""
import pygame, GameLibrary
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((900, 900))
background = pygame.Surface(screen.get_size()).convert()
background.fill((0, 0, 0))


start = pygame.font.SysFont('Gautami', 10)


HighscoreDictionary = {1: [1, ' Winner:', None, ' Colour:', None, ' Number of Moves:', None, ' Length of Game', None], 2: [2,' Winner:',None , ' Colour:',None, ' Number of Moves:',None, ' Length of Game',None], 3: [3,' Winner:',None , ' Colour:',None, ' Number of Moves:',None, ' Length of Game',None], 4: [4,' Winner:',None , ' Colour:',None, ' Number of Moves:',None, ' Length of Game',None], 5: [5,' Winner:',None , ' Colour:',None, ' Number of Moves:',None, ' Length of Game',None]}
#
HighScore = open ("HighscoreValues.csv", "w+")
for NumVal in HighscoreDictionary.values():
    x = ""
    for record in range(0, len(NumVal)):
        if record == len(NumVal)-1:
            x += str(NumVal[record]) + '\n'
        else:
            x += str(NumVal[record]) + ","
    HighScore.write(x)

HighScore.close()

screen.blit(background, (0,0))

x=0
z=0
y=50
showScore = open('HighscoreValues.csv', 'r+')
csvReader1= GameLibrary.openShow(showScore)



Text= next(csvReader1)
for i in range(4):
    for Score in range(9):
        ScoreFont= start.render(Text[z], True,(255, 255, 255))
        screen.blit(ScoreFont, (x, y))
        x+=100
        z+=1
    Text= next(csvReader1)
    z=0
    x=0
    y+=50

pygame.display.flip()

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
