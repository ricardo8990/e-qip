import pygame, sys, math, random
from pygame import *

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

bond = 'bond skiing.png'
WIN_HEIGHT = 400
WIN_WIDTH = 468
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

swallows = pygame.sprite.Group()
screen = pygame.display.set_mode((400, 468))

class Swallow(pygame.sprite.Sprite):
    def __init__(self, width=10, height=10, x=0, y=0, color=GREEN):
        super(Swallow, self).__init__()  # this is for python 2.x users
        #super().__init__(self)
        # self.image and self.rect required for sprite.Group.draw()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.x_subpixel = x
        self.y_subpixel = y
        #pygame.Surface.blit(tree, self.rect, area=None, special_flags = 0)

    # subpixel required for constant movement rate per second
    @property
    def x_subpixel(self):
        return self._x_subpixel
    @x_subpixel.setter
    
    def x_subpixel(self, new_x):
        self._x_subpixel = new_x
        self.rect.x = int(round(new_x))
        
    @property
    def y_subpixel(self):
        return self._y_subpixel
    
    @y_subpixel.setter
    def y_subpixel(self, new_y):
        self._y_subpixel = new_y
        self.rect.y = int(round(new_y))


class Bond(object):
     def __init__(self, x, y, img):
          self.x = x
          self.y = y
          self.img = img
          self.rect = Rect(x,y,34,44)

     def update(self, down, left, right):
          if down:
               self.y = 3
               #self.rect.top += self.y
          if left:
               self.x = -1
               self.rect.left += self.x
          if right:
               self.x = 1
               self.rect.right += self.x

          if self.rect.left<0:
               self.rect.left=0
          elif self.rect.right>468:
               self.rect.right = 468
          elif self.rect.bottom > 1000:
               self.rect.bottom = 1000   ##FINISH GAME
          else:
               self.rect.left += self.x
               self.rect.right += self.x
               self.rect.top += self.y


      
class Background(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = Rect(x,y,468,1000)


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

        
class Camera(object):
     def __init__(self, camera_func, width, height):
          self.camera_func = camera_func
          self.state = Rect(0, 0, width, height)

     def apply(self, target):
          return target.rect.move(self.state.topleft)

     def update(self, target):
          self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
     l, t, _, _ = target_rect
     _, _, w, h = camera
     return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
     l, t, _, _ = target_rect
     _, _, w, h = camera
     l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

     l = min(0, l)                           
     l = max(-(camera.width-WIN_WIDTH), l)   
     t = max(-(camera.height-WIN_HEIGHT), t) 
     t = min(0, t)                          
     return Rect(l, t, w, h)

#def addAgents():

#def addObstacles():

#def handleCollision():

#def showScores():  

def end():
     pygame.quit()
     sys.exit()

global chance_to_appear

global airspeed_velocity


def main():
     pygame.init()
     screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
     pygame.display.set_caption("007 JAMES BOND")
     clock = pygame.time.Clock()

     down = left = right = False
     bnd = pygame.image.load(bond)
     bgimg = pygame.image.load('bg.png')
     total_level_width  = 468
     total_level_height = 1000
     camera = Camera(complex_camera, total_level_width, total_level_height)
     player = Bond(0,0,bnd)
     bg = Background(0,0,bgimg)
  
     pygame.mouse.set_visible(0)
     screen.blit(bgimg,(0,0))

     chance_to_appear = 0.01
     airspeed_velocity = 100
     
     while True:
          ticks = clock.tick(60)
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    end() 
     
               elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                         left = True
                    elif event.key == pygame.K_RIGHT:
                         right = True
                    elif event.key == pygame.K_DOWN:
                         down = True
                 
               elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                         left = False
                    elif event.key == pygame.K_RIGHT:
                         right = False
                    elif event.key == pygame.K_DOWN:
                         down = False


          if random.random() < chance_to_appear:
               swallow = Swallow(x=random.randrange(WIN_WIDTH), y=WIN_HEIGHT)
               swallows.add(swallow)
          for swallow in swallows:
               swallow.y_subpixel -= float(airspeed_velocity) * ticks / 1000
          for swallow in swallows:
               if swallow.y_subpixel <= 0:
                    swallows.remove(swallow)
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    done = True
                    

          screen.fill(WHITE)
          swallows.draw(screen)  # Group.draw uses each .image and .rect to draw
          pygame.display.flip()          
          #screen.blit(bgimg,(camera.apply(bg)))
          camera.update(player)
          player.update(down, left, right)   
          screen.blit(bnd,(camera.apply(player)))
          pygame.display.update()
  
          

          

if __name__ == '__main__':
     main()
