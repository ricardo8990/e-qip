import cmath

import pygame
from pygame import *

pygame.mixer.init(22050, -16, 2, 2096)


class JamesBond(pygame.sprite.Sprite):
    def __init__(self, width, height, name):
        super(JamesBond, self).__init__()
        self.power = 100
        self.lives = 3
        self.dead = False
        self.index = 1
        self.image = pygame.image.load("images/jamesr1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rel_rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.level_width = width
        self.level_height = height
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

    def update(self, down, left, right, camera, obstacles):
        if down:
            self.image = pygame.image.load('images/bond skiing.png').convert_alpha()
            self.y = 3.9
        if left:
            self.image = pygame.image.load("images/ski left.png").convert_alpha()
            self.x = -3
        if right:
            self.image = pygame.image.load("images/ski right.png").convert_alpha()
            self.x = 3

        if self.rel_rect.x + self.x < 0:
            self.rel_rect.x = 0
        elif self.rel_rect.x + self.x > self.level_width - self.image.get_width():
            self.rel_rect.x = self.level_width - self.image.get_width()
        else:
            self.rel_rect.x += self.x

        if self.rel_rect.y + self.y > self.level_height - self.image.get_height():
            self.rel_rect.y = self.level_height - self.image.get_height()
        else:
            self.rel_rect.y += self.y

        self.rect = camera.apply(self)
        self.collide(obstacles)

    def collide(self, obstacles):
        for obstacle in obstacles:
            if self.rel_rect.colliderect(obstacle.rel_rect):
                if isinstance(obstacle, Agent):
                    if self.lives == 0:
                        self.dead = True
                        print "GAME OVER"

                    else:
                        self.lives -= 1
                        self.power = 100
                        self.rel_rect.top += 20
                        obstacle.rel_rect.bottom -= 50

                        # somehow game should start again?

                    print "lives left:", self.lives
                if isinstance(obstacle, Tree):
                    if self.lives == 0:
                        self.dead = True
                        print "GAME OVER"

                    if self.power == 0 and self.lives != 0:
                        self.lives -= 1
                        self.power = 100
                    else:
                        self.power -= 1
                    self.rel_rect.bottom = obstacle.rel_rect.top
                    self.rel_rect.x = self.rel_rect.x
                    print "power: ", self.power
                    return False


class Background(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rel_rect = Rect(x, y, self.img.get_rect().size[0], self.img.get_rect().size[1])


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super(Obstacle, self).__init__()
        self.img = pygame.image.load(image_file).convert_alpha()
        self.rel_rect = Rect(x, y, self.img.get_rect().size[0], self.img.get_rect().size[1])
        self.x = x
        self.y = y


class Tree(Obstacle):
    def __init__(self, x=0, y=0):
        super(Tree, self).__init__(x, y, "images/tree.png")


class Agent(Obstacle):
    def __init__(self, x=0, y=0):
        self.dist = 0
        super(Agent, self).__init__(x, y, "images/agent_skiing.png")

    def track_player(self, player):
        dx, dy = self.rel_rect.x - player.rel_rect.x, self.rel_rect.y - player.rel_rect.y
        self.dist = cmath.sqrt(dx * dx + dy * dy)
        dx, dy = float(dx / self.dist.real), float(dy / self.dist.real)
        self.rel_rect.x -= dx * 3
        self.rel_rect.y -= dy * 4


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rel_rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rel_rect)
