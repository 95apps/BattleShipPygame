import pygame
from pygame.locals import *
import GameLibrary
import numpy as np
pygame.init()


GameXlength= 640
GameYlength= 480

full_size = (GameXlength, GameYlength) # set the screen size
ChipSize = 70

screen = pygame.display.set_mode(full_size)
background = pygame.Surface(full_size).convert()

clock = pygame.time.Clock()
clock.tick(60)#Set Frame Rate

bg_colour = (0, 0, 0) #sets Background
background.fill(bg_colour) #Sets Background Colour


BackGroundImage = pygame.image.load("Connect4Board.png")
BackGroundImage = BackGroundImage.convert_alpha()
screen.blit(BackGroundImage, (0, 0))

PlayerTurn= 0

ChipImageRed = pygame.image.load("RedChip.png")
ChipImageRed = pygame.transform.smoothscale(ChipImageRed, (ChipSize, ChipSize))
ChipImageRed = ChipImageRed.convert_alpha()

ChipImageBlack = pygame.image.load("BlackChip.png")
ChipImageBlack = pygame.transform.smoothscale(ChipImageBlack, (ChipSize, ChipSize))
ChipImageBlack = ChipImageBlack.convert_alpha()

RedChip= False
BlackChip= False


ChipPosition= None

x=0
y=0

y1=0
y2=0
y3=0
y4=0
y5=0
y6=0
y7=0

Tie= False

Falling= False
rect= None

pygame.display.flip()
gameLoop = True

ShowingHighscore= False

playingGame = False

FallLength= GameYlength
board = np.array([[dict([("colour", None), ("isFilled", False)]) for d in range(7)] for l in range(6)])

#BoardBackground = pygame.image.load("Connect4Board.png")

while gameLoop:
    if Falling:
        if RedChip:
            screen.blit(ChipImageRed, rect)
            screen.blit(BackGroundImage, (0, 0))
            rect.y+=10
            if y==0 and rect.y>=410:
                Falling= False
            elif rect.y>=410-80*y:
                Falling= False
        if BlackChip:
            screen.blit(ChipImageBlack, rect)
            screen.blit(BackGroundImage, (0, 0))
            rect.y+=10
            if y==0 and rect.y>=410:
                Falling= False
            elif rect.y>=410-80*y:
                Falling= False



    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONUP: #Searches for button up postion
            GameCursorXPosition = pygame.mouse.get_pos()[0] # Gets X position
            if 0 < GameCursorXPosition <=(GameXlength/7) and y1<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * (29 / 1280), GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * (29 / 1280), GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=0
                y=y1
                y1+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
                print(x)
                print(y)
            elif (GameXlength/7) < GameCursorXPosition<=(2*GameXlength/7)and y2<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 2 * (29 / 1280) + 76, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * 2 * (29 / 1280) + 76, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=1
                y=y2
                y2+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (2*GameXlength/7) < GameCursorXPosition<=(3*GameXlength/7)and y3<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 3 * (29 / 1280) + 76 * 2, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * 3 * (29 / 1280) + 76 * 2 , GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=2
                y=y3
                y3+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (3*GameXlength/7) < GameCursorXPosition<=(4*GameXlength/7)and y4<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 4 * (29 / 1280) + 75.5 * 3, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * 4 * (29 / 1280) + 75.5 * 3, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=3
                y=y4
                y4+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (4*GameXlength/7) < GameCursorXPosition<=(5*GameXlength/7) and y5<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 5 * (29 / 1280) + 75.5 * 4, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    BlackChipPostion=(GameXlength * 5 * (29 / 1280)+75.5*4, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=4
                y=y5
                y5+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (5*GameXlength/7) < GameCursorXPosition<=(6*GameXlength/7)and y6<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 6 * (29 / 1280) + 75.5 * 5, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    BlackChipPostion=(GameXlength * 6 * (29 / 1280)+ 75.5*5, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=5
                y=y6
                y6+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (6*GameXlength/7) < GameCursorXPosition<=(GameXlength)and y7<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 7 * (29 / 1280) + 75.5 * 6, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=[GameXlength * 7 * (29 / 1280) + 75.5 * 6, GameYlength * (7 / 480)]
                    screen.blit(ChipImageBlack, ChipPosition)
                x=6
                y=y7
                y7+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))

        if y1==6 and y2==6 and y3==6 and y4==6 and y5==6 and y6==6 and y7==6:
            Tie=True
        if ev.type == pygame.QUIT:
                gameLoop = False
        else:
            pass
    pygame.display.flip()
import pygame
from pygame.locals import *
import GameLibrary
import numpy as np
pygame.init()


GameXlength= 640
GameYlength= 480

full_size = (GameXlength, GameYlength) # set the screen size
ChipSize = 70

screen = pygame.display.set_mode(full_size)
background = pygame.Surface(full_size).convert()

clock = pygame.time.Clock()
clock.tick(60)#Set Frame Rate

bg_colour = (0, 0, 0) #sets Background
background.fill(bg_colour) #Sets Background Colour


BackGroundImage = pygame.image.load("Connect4Board.png")
BackGroundImage = BackGroundImage.convert_alpha()
screen.blit(BackGroundImage, (0, 0))

PlayerTurn= 0

ChipImageRed = pygame.image.load("RedChip.png")
ChipImageRed = pygame.transform.smoothscale(ChipImageRed, (ChipSize, ChipSize))
ChipImageRed = ChipImageRed.convert_alpha()

ChipImageBlack = pygame.image.load("BlackChip.png")
ChipImageBlack = pygame.transform.smoothscale(ChipImageBlack, (ChipSize, ChipSize))
ChipImageBlack = ChipImageBlack.convert_alpha()

RedChip= False
BlackChip= False


ChipPosition= None

x=0
y=0

y1=0
y2=0
y3=0
y4=0
y5=0
y6=0
y7=0

Tie= False

Falling= False
rect= None

pygame.display.flip()
gameLoop = True

ShowingHighscore= False

playingGame = False

FallLength= GameYlength
board = np.array([[dict([("colour", None), ("isFilled", False)]) for d in range(7)] for l in range(6)])

#BoardBackground = pygame.image.load("Connect4Board.png")

while gameLoop:
    if Falling:
        if RedChip:
            screen.blit(ChipImageRed, rect)
            screen.blit(BackGroundImage, (0, 0))
            rect.y+=10
            if y==0 and rect.y>=410:
                Falling= False
            elif rect.y>=410-80*y:
                Falling= False
        if BlackChip:
            screen.blit(ChipImageBlack, rect)
            screen.blit(BackGroundImage, (0, 0))
            rect.y+=10
            if y==0 and rect.y>=410:
                Falling= False
            elif rect.y>=410-80*y:
                Falling= False



    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONUP: #Searches for button up postion
            GameCursorXPosition = pygame.mouse.get_pos()[0] # Gets X position
            if 0 < GameCursorXPosition <=(GameXlength/7) and y1<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * (29 / 1280), GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * (29 / 1280), GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=0
                y=y1
                y1+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
                print(x)
                print(y)
            elif (GameXlength/7) < GameCursorXPosition<=(2*GameXlength/7)and y2<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 2 * (29 / 1280) + 76, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * 2 * (29 / 1280) + 76, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=1
                y=y2
                y2+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (2*GameXlength/7) < GameCursorXPosition<=(3*GameXlength/7)and y3<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 3 * (29 / 1280) + 76 * 2, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * 3 * (29 / 1280) + 76 * 2 , GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=2
                y=y3
                y3+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (3*GameXlength/7) < GameCursorXPosition<=(4*GameXlength/7)and y4<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 4 * (29 / 1280) + 75.5 * 3, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=(GameXlength * 4 * (29 / 1280) + 75.5 * 3, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=3
                y=y4
                y4+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (4*GameXlength/7) < GameCursorXPosition<=(5*GameXlength/7) and y5<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 5 * (29 / 1280) + 75.5 * 4, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    BlackChipPostion=(GameXlength * 5 * (29 / 1280)+75.5*4, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=4
                y=y5
                y5+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (5*GameXlength/7) < GameCursorXPosition<=(6*GameXlength/7)and y6<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 6 * (29 / 1280) + 75.5 * 5, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    BlackChipPostion=(GameXlength * 6 * (29 / 1280)+ 75.5*5, GameYlength * (7 / 480))
                    screen.blit(ChipImageBlack, ChipPosition)
                x=5
                y=y6
                y6+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))
            elif (6*GameXlength/7) < GameCursorXPosition<=(GameXlength)and y7<6:
                if PlayerTurn%2==0:
                    RedChip= True
                    BlackChip= False
                    ChipPosition=(GameXlength * 7 * (29 / 1280) + 75.5 * 6, GameYlength * (7 / 480))
                    screen.blit(ChipImageRed, ChipPosition)
                else:
                    BlackChip=True
                    RedChip= False
                    ChipPosition=[GameXlength * 7 * (29 / 1280) + 75.5 * 6, GameYlength * (7 / 480)]
                    screen.blit(ChipImageBlack, ChipPosition)
                x=6
                y=y7
                y7+=1
                if y<=6:
                    board[y][x]["isFilled"] = True
                if RedChip:
                    board[y][x]["colour"] = "red"
                elif BlackChip:
                    board[y][x]["colour"] = "black"
                PlayerTurn += 1
                Falling= True
                rect= Rect((ChipPosition),(ChipSize, ChipSize))

        if y1==6 and y2==6 and y3==6 and y4==6 and y5==6 and y6==6 and y7==6:
            Tie=True
        if ev.type == pygame.QUIT:
                gameLoop = False
        else:
            pass
    pygame.display.flip()
