# -*- coding: utf-8 -*-
# By Daniel Petri 2012-2014. Graphics by Paulo Ditzel and Peter Pluecker.
# Special thanks to Michail (michailgames.com)
# Check out the 'Encyclopedia' README file to discover how this code works
# -*- CC BY-NC 4.0 -*-

import pygame, sys, math, random
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled!')
if not pygame.mixer:
    print('Warning, sound disabled!')

bg = 'data/background/bg.jpg'
ship = 'data/living/ship.png'
meteor = 'data/rocks/meteor.png'
meteor_debris = 'data/rocks/meteor_debris.png'
earth = 'data/rocks/earth.png'
mars = 'data/rocks/mars.png'
jupiter = 'data/rocks/jupiter.png'
enemyship1 ='data/living/enemyship1.png'
enemyship2 = 'data/living/enemyship2.png'
enemyship3 = 'data/living/enemyship3.png'
playermissile1 = 'data/effects/playermissile1.png'

pygame.init()

#sound setup below (for future use)

class Player(object):
    def __init__(self, x, y, img, health, shield, meteor_collision, ship_collision, shooting):
        self.x = x
        self.y = y
        self.img = img
        self.health = health
        self.shield = shield
        self.meteor_collision = meteor_collision
        self.ship_collision = ship_collision
        self.shooting = shooting
        
class Background(object):
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed

class Meteor(object):
    def __init__(self, x, y, img, degrees, direction, defaultimg):
        self.x = x
        self.y = y
        self.img = img
        self.degrees = degrees
        self.direction = direction
        self.rotated = img
        self.defaultimg = defaultimg

class Planet(object):
    def __init__(self, x, y, img, size):
        self.x = x
        self.y = y
        self.img = img
        self.size = size

class Ship(object):
    def __init__(self, x, y, img, speed, speedy, degrees):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.speedy = speedy
        self.degrees = degrees

class Bullet(object):
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed

WIDTH = 960 # x coord
HEIGHT = 720 # y coord

#Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (192,0,0)
YELLOW = (238,201,0)
GREEN = (50, 205, 50)

astroFont = pygame.font.Font('data/font/astro.ttf',20)

screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
pygame.display.set_caption("Nebula Wars 0.3")

#Sprites
bg = pygame.image.load(bg).convert()
ship = pygame.image.load(ship).convert_alpha()
meteor = pygame.image.load(meteor).convert_alpha()
meteor_debris = pygame.image.load(meteor_debris).convert_alpha()
earth = pygame.image.load(earth).convert_alpha()
mars = pygame.image.load(mars).convert_alpha()
jupiter = pygame.image.load(jupiter).convert_alpha()
enemyship1 = pygame.image.load(enemyship1).convert_alpha()
enemyship2 = pygame.image.load(enemyship2).convert_alpha()
enemyship3 = pygame.image.load(enemyship3).convert_alpha()
playermissile1 = pygame.image.load(playermissile1).convert_alpha()

fpsClock = pygame.time.Clock()

#Classes
player=Player(0, 0, ship, 100, 100, False, False, False) # x, y, img, health, shield, meteor_collision, ship_collision, shooting
background=Background(0, 0, bg, 1)
meteor=Meteor(960, 180, meteor, 0, -1, meteor)
planet=Planet(960, 360, earth, 3)
ship=Ship(960, 360, enemyship1, 3, 0, 0)
bullet=Bullet(WIDTH, 0, playermissile1, 13)

def addRocks():
    screen.blit(planet.img, (planet.x, planet.y)) #Draws
    screen.blit(meteor.img, (meteor.x, meteor.y))
    
    #=======================Planet=====================#
    if planet.size == 1:
        planet.img = pygame.transform.scale(planet.img, (70, 72))
        planet.x -= 2
    elif planet.size == 2:
        planet.img = pygame.transform.scale(planet.img, (140, 144))
        planet.x -= 3
    else:
        planet.img = pygame.transform.scale(planet.img, (280, 288))
        planet.x -= 4
        
    if planet.x < -300:
       planet.img = random.randint(1,3)
       if planet.img == 3:
           planet.img = earth
       if planet.img == 2:
           planet.img = mars
       if planet.img == 1:
          planet.img = jupiter
       planet.size = random.randint(1,3)
       planet.x = 980
       planet.y = random.randint(100, 500)
       
    #=======================Meteor=====================#
    meteor.x -= 8 #Speed
    meteor.y += meteor.direction  #Direction
    
    meteor.img = pygame.transform.rotate(meteor.rotated, meteor.degrees)
    meteor.degrees += 1

    if player.meteor_collision == True:
        meteor.rotated = meteor_debris

    else:
        meteor.rotated = meteor.defaultimg
        
    if meteor.x <= -120 or meteor.y > HEIGHT+120 or meteor.y < -120: #Makes meteor go back if it leaves the window or crashes into the player's ship
       meteor.x = random.randint(960, 1000)
       meteor.y = random.randint(50, 720)
       meteor.direction *= -1
       player.meteor_collision = False
       meteor.img = meteor.defaultimg

def addShips():
    if not player.ship_collision:
        screen.blit(ship.img, (ship.x, ship.y)) #Draws enemy ship
    screen.blit(player.img, (player.x, player.y)) #Draws player ship

    ship.x -= ship.speed #Moves ship sideways
    
    if ship.x > 780: #Moves ship a little bit up
        ship.y += ship.speedy

    if ship.img == enemyship1: #Speed variation
        ship.speed = 3
        if ship.x < 640:
            ship.speed = 15
            
    if ship.img == enemyship2:
        ship.speed = 7
        
    if ship.img == enemyship3:
        ship.speed = 5
        
    if ship.x <= -120 or ship.y > HEIGHT+120 or ship.y < -120: #Checks if ship is offscreen. If so, adds a new one
       player.ship_collision = False # Ship collision is always set to False when it spawns
       ship.degrees = 0 #Same applies to it's rotation
       
       ship.img = random.randint(1,3) #Change the type of a random ship
       if ship.img == 3:
           ship.img = enemyship3
       if ship.img == 2:
           ship.img = enemyship2
       if ship.img == 1:
           ship.img = enemyship1
           
       ship.x = random.randint(960, 1000)
       ship.y = random.randint(50, 650)

       if ship.speedy >= 0: #Controls ship AI direction
           ship.speedy *= -1
       
       if ship.y > 360: #Selects random Y direction
           ship.speedy += 0.5

       else:
           ship.speedy -= 0.5
           
def animateBackground():
    screen.blit(background.img, (background.x, background.y)) #BG 1
    screen.blit(background.img, (background.x+WIDTH, background.y)) #BG 2

    background.x -= background.speed

    if background.x <= -960:
        background.x = 0

def drawText(text, font, x, y, color):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        screen.blit(textobj, textrect)

def shoot():    
    if player.shooting == True:
        screen.blit(bullet.img, (bullet.x, bullet.y)) #Blits bullet's image
        if bullet.x < WIDTH:
            bullet.x += bullet.speed

def collisionBoxes(): #Draws collision boxes and checks for them. Note to self: screen, color, (x, y, width, height), thickness
    ##Player##
    playerRect = [pygame.Rect(player.x+35, player.y+28, 60, 5), #Creates multiple collision rectangles
                  pygame.Rect(player.x+40, player.y+35, 50, 5),
                  pygame.Rect(player.x, player.y+16, 40, 10),
                  pygame.Rect(player.x+16, player.y+10, 10, 5),
                  pygame.Rect(player.x+85, player.y+5, 52, 13)]

    playerBox = list(playerRect)

    #for rect in playerBox: pygame.draw.rect(screen, GREEN, rect, 1) #Allows you to see collision boxes
    #pygame.draw.rect(screen, WHITE, (player.x, player.y, 148, 43), 1)

    ##Meteor##
    meteorBox = pygame.Rect((meteor.x+10), (meteor.y+10), 56, 43)
    #pygame.draw.rect(screen, WHITE, meteorBox, 1)

    ##Enemy Ship##
    if ship.img == enemyship1:
        if ship.x > 640:                                       ###
            shipBox = pygame.Rect(ship.x, ship.y, 43, 11)      ###
            #pygame.draw.rect(screen, WHITE, shipBox, 1)       ###
                                                               ### Prevents a lag in enemyship1's collision box when he boosts
        else:                                                  ###
            shipBox = pygame.Rect((ship.x+13), ship.y, 43, 11) ###
            #pygame.draw.rect(screen, WHITE, shipBox, 1)       ###

    elif ship.img == enemyship2:
        shipBox = pygame.Rect((ship.x+5), ship.y, 70, 20)
        #pygame.draw.rect(screen, WHITE, shipBox, 1)

    elif ship.img == enemyship3:
        shipBox = pygame.Rect(ship.x+6, ship.y, 72, 46)
        #pygame.draw.rect(screen, WHITE, shipBox, 1)

    ##Bullet##
    bulletBox = pygame.Rect(bullet.x, bullet.y, 95, 17)
    #pygame.draw.rect(screen, YELLOW, bulletBox, 1)
    
    ############# Actual collision #############

    #If a player crashes into a meteor
    if player.meteor_collision == False:
        if player.health >= 0 and meteor.rotated != meteor_debris:
            for r1 in playerBox:
                if r1.colliderect(meteorBox):    
                    player.meteor_collision = True
                    player.health -= ((1-(player.shield/100))*random.randint(30,50)) # The higher your shield, the less damage you take.
                    player.shield -= random.randint(15, 30)

    #If a player crashes into a ship
    def dropShip(): #Controls ship's death animation
        ship.y += 15
        ship.x -= 3
        shipDropping = pygame.transform.rotate(ship.img, ship.degrees)
        screen.blit(shipDropping, (ship.x, ship.y))
        ship.degrees -= 3 #Similar code to how the meteor's rotation works
    
    if player.ship_collision == False:
        for r1 in playerBox:
            if r1.colliderect(shipBox):
                player.ship_collision = True
                if ship.img == enemyship1:
                    if ship.x < 640: # Tiny enemy ship is moving fast... lots of damage shall be taken
                        player.health -= ((1-(player.shield/100))*random.randint(20,40))
                        player.shield -= random.randint(10, 20)

                    else: # Tiny enemy is moving slowly
                        player.health -= ((1-(player.shield/100))*random.randint(5,12))
                        player.shield -= random.randint(2, 7)

                elif ship.img == enemyship2:
                    player.health -= ((1-(player.shield/100))*random.randint(15,25))
                    player.shield -= random.randint(19, 26)

                else:
                    player.health -= ((1-(player.shield/100))*random.randint(27,37))
                    player.shield -= random.randint(28, 44)
                                       
    if player.ship_collision: #Starts ship's death animation
        dropShip()

    #If a bullet crashes into a ship
    if bulletBox.colliderect(shipBox):
        player.ship_collision = True

    #If a bullet crashes into a meteor
    if bulletBox.colliderect(meteorBox):
        player.meteor_collision = True
        
    ############# Dying and making sure your stats don't reach negative numbers #############
    if player.health <= 0:
        drawText('Game over', astroFont, 400, 300, WHITE)
        player.health = 0

    if player.shield < 0:
        player.shield = 0
    
def draw():
    animateBackground()
    shoot()
    addRocks()
    addShips()
    collisionBoxes()

    li = [round(player.health),player.shield]
    #Different display colors
    if player.health >= 90:
        drawText('healTh: {0} shielD: {1}'.format(*li), astroFont, 5, 5, WHITE)
    elif player.health >= 60 and player.health < 90:
        drawText('healTh: {0} shielD: {1}'.format(*li), astroFont, 5, 5, GREEN)
    elif player.health >= 40 and player.health < 60:
        drawText('healTh: {0} shielD: {1}'.format(*li), astroFont, 5, 5, YELLOW)
    else: # player.health >= 0 and player.health < 40:
        drawText('healTh: {0} shielD: {1}'.format(*li), astroFont, 5, 5, RED)
    ##########################
    
def getEvents():
    FULLSCREENMODE = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            end()

        if event.type == MOUSEBUTTONDOWN:
            if bullet.x >= WIDTH: # Makes sure you can't shoot more than one bullet if one has already been shot
                bullet.x = player.x + 70 #Sets bullets coords for new shot
                bullet.y = player.y + 5

                player.shooting = True
            
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                end()
            
            elif event.key == K_F11:
                FULLSCREENMODE = not FULLSCREENMODE
                if FULLSCREENMODE:
                    screen = pygame.display.set_mode((WIDTH,HEIGHT), FULLSCREEN) #Fullscreen
                else:
                    screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32) #Windowed

    player.x, player.y = pygame.mouse.get_pos() #
    player.x -= player.img.get_width()/2 # mouse control
    player.y -= player.img.get_height()/2 #

def end():
    pygame.quit()
    sys.exit()

def main():
    while True:
        getEvents()
        draw()
        fpsClock.tick(30)
        pygame.display.update()

if __name__ == '__main__':
    main()
