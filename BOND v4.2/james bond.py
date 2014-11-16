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


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)
    return Rect(l, t, w, h)

def print_text(screen, text, x, y, size, colour):
    game_font = pygame.font.Font(None, size)
    text_render = game_font.render(text, 1, colour)
    text_rect = text_render.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text_render, text_rect)

def show_points(screen, player):
    first_line_text = "Power: %d" % player.power
    second_line_text = "Lives: %d" % player.lives
    print_text(screen, first_line_text, 0, 70, 15, BLACK)
    print_text(screen, second_line_text, 0, 80, 15, BLACK)


def start_animation(james, screen, all_sprites_list, clock, bgimg):
    while james.rect.x <= animation_end_point[0]:
        screen.blit(bgimg, (0, 0))
        james.update_animation()
        all_sprites_list.draw(screen)
        clock.tick(20)
        pygame.display.flip()

def addTrees(total_level_width,total_level_height, obstacle_loc,obstacles):
    for i in range (70):        #maps the trees
        row = random.randint(10,total_level_width-10)
        col = random.randint(animation_end_point[0], total_level_height-80)
        location  = [row, col]
        if not (location in obstacle_loc):      #makes sure two trees are not in the same location
            obstacle_loc.append(location)
            tree = Classes.Tree(location[0], location[1])
            obstacles.add(tree)


def addAgents(total_level_width,total_level_height, obstacle_loc,obstacles):
    for i in range (2):        #maps the agents
        row = random.randint(10,total_level_width-30)
        col = random.randint(animation_end_point[0]-50,animation_end_point[0]+50)
        location  = [row, col]
        if not (location in obstacle_loc):      #makes sure two agents are not in the same location
            obstacle_loc.append(location)
            agent = Classes.Agent(location[0], location[1])
            obstacles.add(agent) 

def end():
    pygame.quit()
    sys.exit()


def main():
    #Initialize variables and window
    pygame.init()
    global WIN_HEIGHT, WIN_WIDTH, HALF_WIDTH, HALF_HEIGHT
    end_screen = pygame.image.load('images/GameOver.png')
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
    flag_agents = 0
    obstacle_loc = []
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
                
                addTrees(total_level_width,total_level_height,obstacle_loc,obstacles)
                
                start_animation(james, screen, all_sprites_list, clock, bgimg)
                screen.blit(bgimg, (0, 0))
                james.dress_to_ski()
                all_sprites_list.draw(screen)
                pygame.display.flip()
                
                while james.dead == False:
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
                    if james.rel_rect.y>animation_start_point[1]+300 and flag_agents==0:
                        addAgents(total_level_width,total_level_height,obstacle_loc,obstacles)
                        flag_agents = 1
                    screen.blit(bgimg, (camera.apply(bg)))
                    camera.update(james)
                    james.update(down, left, right, camera,obstacles)
                    show_points(screen, james)
                    screen.blit(james.image,(camera.apply(james)))
                    for obstacle in obstacles:
                        if isinstance (obstacle,Classes.Agent):
                            #if obstacle.rel)rect
                            obstacle.trackPlayer(james)
                        screen.blit(obstacle.img, (camera.apply(obstacle)))
                    pygame.display.update()
                    
                #ends game in a terrible way...
                screen.blit(end_screen,(0,0))
                pygame.time.delay(300)
                pygame.display.update()
                pygame.time.delay(5000)
                end()


if __name__ == '__main__':
    main()