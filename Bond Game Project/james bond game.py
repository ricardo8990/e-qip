import pygame, sys, math, random
from pygame.locals import *

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

bond = 'bond skiing.png'
background = 'snow.jpg'



class Bond(object):
     def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

class Background(object):
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed

class Agent(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
class Obstacle(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        

     

pygame.init()
   
size = [700, 500]
screen = pygame.display.set_mode(size)
  
pygame.display.set_caption("007 JAMES BOND")

bond = pygame.image.load(bond)
background = pygame.image.load(background)

player = Bond(350,10,bond)
bg = Background(0,0,background,1)
done = False
  
clock = pygame.time.Clock()
 
pygame.mouse.set_visible(0)

def animateBackground():
    screen.blit(background, (bg.x, bg.y))
    screen.blit(background, (bg.x, bg.y+size[1]))

    bg.y -= bg.speed

    if bg.y <= -500:
        bg.y = 0

#def addAgents():

#def addObstacles():

#def handleCollision():

#def showScores():
        

def end():
    pygame.quit()
    sys.exit()

def getEvents():

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            end() 
     
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= 5
            elif event.key == pygame.K_RIGHT:
                player.x += 5
            elif event.key == pygame.K_UP:
                player.y -= 5
            elif event.key == pygame.K_DOWN:
                player.y += 5
                  
        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                player.x=player.x
            elif event.key == pygame.K_RIGHT:
                player.x=player.x
            elif event.key == pygame.K_UP:
                player.y=player.y
            elif event.key == pygame.K_DOWN:
                player.y=player.y



def main():
    while True:
        animateBackground()
        getEvents()

        screen.blit(bond,(player.x,player.y))
  
        pygame.display.update()
  
        clock.tick(60)

if __name__ == '__main__':
    main()
