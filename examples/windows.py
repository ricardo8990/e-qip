import sys
import pygame
from pygame.locals import *
from random import randint

pygame.init()
infoObject = pygame.display.Info()

window = pygame.display.set_mode((infoObject.current_w / 2, infoObject.current_h / 2))
pygame.display.set_caption("Hello world")

colour = (70, 80, 150)
##Draw a line
#pygame.draw.line(window, colour, (60, 80), (160, 100), 20)
##Draw a circle
#pygame.draw.circle(window, colour, (80, 90), 40)
##Draw a rectangle
#pygame.draw.rect(window, (40, 50, 60), (150, 100, 100, 50))
##Draw a polygon
#pygame.draw.polygon(window, (20, 60, 134), ((300, 45), (230, 54), (50, 260)))
#Load an image
image = pygame.image.load("Images/gorill.gif")
posX = 200          # randint(10, 20)
posY = 100
speed = 20
blackColour = (0, 0, 0)
isRight = True

while True:
    window.fill(blackColour)
    window.blit(image, (posX, posY))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                posX -= speed
            elif event.key == K_RIGHT:
                posX += speed
            elif event.key == K_UP:
                posY -= speed
            elif event.key == K_DOWN:
                posY += speed

    #Uncomment to follow the mouse
    #posX, posY = pygame.mouse.get_pos()

    # ##Animacion
    # if isRight:
    #     if posX <= 400:
    #         posX += speed
    #     else:
    #         isRight = False
    # else:
    #     if posX > 1:
    #         posX -= speed
    #     else:
    #         isRight = True

    pygame.display.update()