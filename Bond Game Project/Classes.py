import pygame
from pygame import *

airspeed_velocity = 100
pygame.mixer.init(22050, -16, 2, 2096)


class JamesBond(pygame.sprite.Sprite):
    def __init__(self, width, height, name):
        super(JamesBond, self).__init__()
        self.index = 1
        self.image = pygame.image.load("images/jamesr1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rel_rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.level_width = width
        self.level_height = height
        self.points = 0
        self.lives = 3
        self.isPlaying = False
        self.name = name
        self.theme1 = pygame.mixer.Sound("main_theme.wav")
        self.bond_voice = pygame.mixer.Sound("sc_bond.wav")

    def update_animation(self):
        self.bond_voice.play()
        self.theme1.play(-1)
        self.rect.x += 3
        self.index = self.index + 1 if self.index < 8 else 1
        image_name = "images/jamesr{}.png".format(self.index)
        self.image = pygame.image.load(image_name).convert_alpha()

    def first_screen(self):
        self.image = pygame.image.load('images/title_screen.jpg')

    def dress_to_ski(self):
        self.rect.x += 45
        self.rel_rect = self.rect
        self.image = pygame.image.load('images/bond skiing.png').convert_alpha()

    def update(self, down, left, right, camera):
        if down:
            self.image = pygame.image.load('images/bond skiing.png').convert_alpha()
            self.y = 3
            self.isPlaying = True
        if left:
            self.image = pygame.image.load("images/ski left.png").convert_alpha()
            self.x = -1
        if right:
            self.image = pygame.image.load("images/ski right.png").convert_alpha()
            self.x = 1

        if self.rel_rect.x + self.x < 0:
            self.rel_rect.x = 0
        elif self.rel_rect.x + self.x > self.level_width - self.image.get_width():
            self.rel_rect.x = self.level_width - self.image.get_width()
        else:
            self.rel_rect.x += self.x

        if self.rel_rect.y + self.y > self.level_height - self.image.get_height():
            self.rel_rect.y = self.level_height - self.image.get_height()
            self.isPlaying = False
        else:
            self.rel_rect.y += self.y

        self.rect = camera.apply(self)

        if self.isPlaying:
            self.points += 50

class Background(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rel_rect = Rect(x, y, 468, 1000)


class Agent(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_y_position(self, y):
        self.rect.y = y

    def get_y_position(self):
        return self.rect.y

    def set_x_position(self, x):
        self.rect.x = x

    def get_x_position(self):
        return self.rect.x

    def update(self, ticks):
        self.rect.y -= float(airspeed_velocity) * ticks / 1000


class Tree(Obstacle):
    def __init__(self, x=0, y=0):
        super(Tree, self).__init__(x, y, "images/tree.png")


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rel_rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rel_rect)
