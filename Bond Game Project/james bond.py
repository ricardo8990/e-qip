import pygame, sys, math, random
from pygame import *

BLACK = (   0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (   0, 255, 0)
RED = ( 255, 0, 0)

bond = 'images/bond skiing.png'
WIN_HEIGHT = 400
WIN_WIDTH = 468
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30
animation_start_point = (0, 90)
animation_end_point = (208, 90)


# ----------------------------------------------------#
#               Class definitions                    #
#----------------------------------------------------#
class JamesBond(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(JamesBond, self).__init__()
        self.index = 1
        self.image = pygame.image.load("images/jamesr1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.level_width = width
        self.level_height = height

    def update_animation(self):
        self.rect.x += 3
        self.index = self.index + 1 if self.index < 8 else 1
        image_name = "images/jamesr{}.png".format(self.index)
        self.image = pygame.image.load(image_name).convert_alpha()

    def dress_to_ski(self):
        self.rect.x += 45
        self.image = pygame.image.load(bond).convert_alpha()

    def update(self, down, left, right):
        if down:
            self.image = pygame.image.load(bond).convert_alpha()
            self.y = 3
        if left:
            self.image = pygame.image.load("images/ski left.png").convert_alpha()
            self.x = -1
        if right:
            self.image = pygame.image.load("images/ski right.png").convert_alpha()
            self.x = 1

        self.rect.y = self.y + self.rect.y if self.rect.y + self.y < self.level_height - self.image.get_height() else self.level_height - self.image.get_height()
        self.rect.x = self.x + self.rect.x if self.rect.x + self.x > 0 else 0
        if self.rect.x > self.level_width - self.image.get_width():
            self.rect.x = self.level_width - self.image.get_width()

class Background(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = Rect(x, y, 468, 1000)


class Agent(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super(Tree, self).__init__()
        self.image = pygame.image.load("images/tree.png").convert_alpha()
        self.rect = self.image.get_rect()


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
    return Rect(-l + HALF_WIDTH, -t + HALF_HEIGHT, w, h)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)
    return Rect(l, t, w, h)


def start_animation(james, screen, all_sprites_list, clock, bgimg):
    while james.rect.x <= animation_end_point[0]:
        screen.blit(bgimg, (0, 0))
        james.update_animation()
        all_sprites_list.draw(screen)
        clock.tick(20)
        pygame.display.flip()

# def addAgents():

#def addObstacles():

#def handleCollision():

#def showScores():  

def end():
    pygame.quit()
    sys.exit()


def main():
    #Initialize variables and window
    pygame.init()
    global WIN_HEIGHT, WIN_WIDTH, HALF_WIDTH, HALF_HEIGHT

    bgimg = pygame.image.load('images/bg.png')
    total_level_width = bgimg.get_width()
    total_level_height = bgimg.get_height()

    info_object = pygame.display.Info()
    WIN_HEIGHT = info_object.current_h / 2 if (info_object.current_h / 2) < total_level_height else total_level_height
    WIN_WIDTH = info_object.current_w / 2 if (info_object.current_w / 2) < total_level_width else total_level_width
    HALF_WIDTH = int(WIN_WIDTH / 2)
    HALF_HEIGHT = int(WIN_HEIGHT / 2)

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FLAGS, DEPTH)
    pygame.display.set_caption("007 JAMES BOND")
    clock = pygame.time.Clock()

    #Initialize objects
    james = JamesBond(total_level_width, total_level_height)
    james.rect.x, james.rect.y = animation_start_point

    all_sprites_list = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    for i in range(5):
        # This represents a tree
        tree = Tree()
        # Set a random location for the tree
        tree.rect.x = random.randrange(WIN_WIDTH)
        tree.rect.y = random.randrange(WIN_HEIGHT)
        # Add the block to the list of objects
        obstacles.add(tree)
        all_sprites_list.add(tree)

    all_sprites_list.add(james)
    down = left = right = False

    camera = Camera(complex_camera, total_level_width, total_level_height)

    bg = Background(0, 0, bgimg)

    pygame.mouse.set_visible(0)

    start_animation(james, screen, all_sprites_list, clock, bgimg)
    screen.blit(bgimg, (0, 0))
    james.dress_to_ski()
    all_sprites_list.draw(screen)
    pygame.display.flip()

    while True:
        clock.tick(60)
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

        screen.blit(bgimg, (camera.apply(bg)))
        camera.update(james)
        james.update(down, left, right)
        all_sprites_list.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
