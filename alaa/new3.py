import pygame, GameLibrary
from pygame.locals import *
from textwrap import fill
pygame.init()

RulesWidth= 1000
RulesLength= 900
screen = pygame.display.set_mode((RulesWidth, RulesLength))
background = pygame.Surface(screen.get_size()).convert()
background.fill((0, 0, 0))

MyFont = pygame.font.SysFont('Gautami', 25)

MyFont2 = pygame.font.SysFont('Gautami', 50)
MyFont2.set_bold(True)
MyFont2.set_underline(True)
RulesFont= MyFont2.render("Rules", True, (255, 255, 255))

RulesText1=[" Click On Screen To See Next Line",
            " The Rules of this game are very similar to the rules of Connect 4.",
            " This is a two player game where you are attempting to get 4 of the same colour chips after each other before your opponent.",
            " This can be vertically horizontally or diagonally.",
            " Here is an example"]


MenuBackground = pygame.image.load("MenuBackground.jpg")

BackButton= pygame.image.load("BackButton.png")

BackButton =  pygame.transform.smoothscale(BackButton, (100, 100))

BackButtonPress=1

screen.blit(MenuBackground, (-500, -50))
screen.blit(RulesFont, (RulesWidth / 2.25, 0))
screen.blit(BackButton,(0,RulesLength-100))


x=0
y=100

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == MOUSEBUTTONDOWN:
            RulesCursorXPosition = pygame.mouse.get_pos()[0]
            RulesCursorYPosition = pygame.mouse.get_pos()[1]
            if  0 < RulesCursorXPosition < 100 and RulesLength-100 < RulesCursorYPosition < RulesLength:
                BackButtonPress-=1
            else:
                BackButtonPress+=1

            if 1 < BackButtonPress < 5:
                Page1Font= MyFont.render(RulesText1[BackButtonPress],True, (255, 255, 255))
                screen.blit(Page1Font,(x,y))
                y+=25
        if ev.type == QUIT:
            keep_going = False

    pygame.display.flip()
