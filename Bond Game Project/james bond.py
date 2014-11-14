import pygame, sys, math, random, Classes
from pygame import *

BLACK = (   0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (   0, 255, 0)
RED = ( 255, 0, 0)

bond = 'images/bond skiing.png'
theme1 = pygame.mixer.Sound("bond.wav")
title_screen = 'images/scr2.jpg'
WIN_HEIGHT = 400
WIN_WIDTH = 468
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30
animation_start_point = (0, 90)
animation_end_point = (208, 90)


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

# def addObstacles():

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
    theme1.play()
    
    
    while(True):
        
        first_screen = pygame.image.load(title_screen)
        screen.blit(first_screen,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                pygame.mixer.pause()
                #Initialize objects
                james = Classes.JamesBond(total_level_width, total_level_height)
                james.rect.x, james.rect.y = animation_start_point

                all_sprites_list = pygame.sprite.Group()
                obstacles = pygame.sprite.Group()

                all_sprites_list.add(james)
                down = left = right = False

                camera = Classes.Camera(complex_camera, total_level_width, total_level_height)

                bg = Classes.Background(0, 0, bgimg)

                pygame.mouse.set_visible(0)

                start_animation(james, screen, all_sprites_list, clock, bgimg)
                screen.blit(bgimg, (0, 0))
                james.dress_to_ski()
                all_sprites_list.draw(screen)
                pygame.display.flip()
                chance_to_appear = 0.01

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
                        tree = Classes.Tree(random.randrange(WIN_WIDTH), WIN_HEIGHT)
                        obstacles.add(tree)
                        all_sprites_list.add(tree)
                    for obstacle in obstacles:
                        obstacle.update(ticks)
                    for obstacle in obstacles:
                        if obstacle.get_y_position() <= 0:
                            obstacles.remove(obstacle)
                            all_sprites_list.remove(obstacle)

                    screen.blit(bgimg, (camera.apply(bg)))
                    camera.update(james)
                    james.update(down, left, right, camera)
                    all_sprites_list.draw(screen)
                    camera.apply(james)
                    pygame.display.update()


if __name__ == '__main__':
    main()
