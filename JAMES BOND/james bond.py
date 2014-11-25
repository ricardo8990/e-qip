import random
import sys
import pygame
from pygame import *
import time
import Classes


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

bond = 'images/bond skiing.png'
theme1 = pygame.mixer.Sound("bond.wav")
heli_sound = pygame.mixer.Sound("sounds/heli.wav")
title_screen = 'images/scr3.jpg'
escape = pygame.image.load('images/esc.png')
end_screen = pygame.image.load('images/GameOver.png')
WIN_HEIGHT = 800
WIN_WIDTH = 868
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
    third_line_text = "Mission: %d" % player.mission
    print_text(screen, player.name, 0, 60, 15, BLACK)
    print_text(screen, first_line_text, 0, 70, 15, BLACK)
    print_text(screen, second_line_text, 0, 80, 15, BLACK)
    print_text(screen, third_line_text, 0, 90, 15, BLACK)


def start_animation(james, screen, all_sprites_list, clock, bgimg, level):
    r = 70
    while james.rect.x <= animation_end_point[0]:
        screen.blit(bgimg, (0, 0))
        james.update_animation()
        text = "LEVEL {}".format(level)
        print_text(screen, text, WIN_WIDTH / 2 - len(text), WIN_HEIGHT / 2, r, BLACK)
        all_sprites_list.draw(screen)
        clock.tick(20)
        pygame.display.flip()
        r -= 1


def show_intro(screen):
    theme1.play(-1)
    first_screen = pygame.image.load(title_screen)
    text_x = 30
    text_y = int(9 * WIN_HEIGHT / 10)
    name = ""
    completed = False

    while not completed:
        screen.blit(first_screen, (0, 0))
        print_text(screen, "Name: ", text_x, text_y, 30, BLACK)
        if name != "":
            print_text(screen, "Enter to continue...", text_x, WIN_HEIGHT - 20, 20, BLACK)
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN and name != "":
                    completed = True
        print_text(screen, name, 100, text_y, 30, BLACK)
        pygame.display.flip()

    pygame.mixer.pause()
    return name


def add_trees(total_level_width, total_level_height, obstacle_loc, obstacles):
    for i in range(20):  # maps the trees 70
        row = random.randint(30, total_level_width - 30)
        col = random.randint(animation_end_point[0], total_level_height - 120)
        location = [row, col]
        if not (location in obstacle_loc):  # makes sure two trees are not in the same location
            obstacle_loc.append(location)
            tree = Classes.Tree(location[0], location[1])
            obstacles.add(tree)


def add_agents(total_level_width, obstacle_loc, obstacles):
    for i in range(2):  # maps the agents
        row = random.randint(10, total_level_width - 30)
        col = random.randint(animation_end_point[0] - 50, animation_end_point[0] + 50)
        location = [row, col]
        if not (location in obstacle_loc):  # makes sure two agents are not in the same location
            obstacle_loc.append(location)
            agent = Classes.Agent(location[0], location[1])
            obstacles.add(agent)


def add_coins(total_level_width, total_level_height, obstacle_loc, obstacles):
    for i in range(10):  # maps the coins
        row = random.randint(50, total_level_width - 50)
        col = random.randint(animation_end_point[0], total_level_height - 300)

        for j in range(4):
            col += 80
            location = [row, col]
            # print "i*20:", location
            if not (location in obstacle_loc):  # makes sure two coins are not in the same location
                # print location
                obstacle_loc.append(location)
                coin = Classes.Coin(location[0], location[1])
                obstacles.add(coin)


def score_sheet(screen, name, player):
    write_file = open("high_score.txt", "a")
    write_file.write("{},".format(name))
    write_file.write("{}\n".format(player.mission))
    write_file.close()

    read_file = open("high_score.txt", "r")
    d = {}
    for line in read_file:
        x = line.split(",")
        a = x[0]
        b = int(x[1])
        # c = len(b)-1
        # b = b[0:c]
        d[a] = b
    read_file.close()
    sortedKey = reversed(sorted(d.items(), key=lambda t: t[1]))
    count = 0
    text_x = 250
    print "--------HIGH SCORE---------"

    for i in sortedKey:
        line = i[0] + '\t' + str(i[1])
        print line
        n = 0
        t_width = 10
        for z in range(2):
            print_text(screen, str(i[n]), t_width, text_x, 25, BLACK)
            t_width += 70
            n += 1
        count += 1
        if count >= 5:
            break

        text_x += 20
        # pygame.display.flip()

    """
    text_x = 30
    N = 5
    screen.blit(end_screen, (0, 0))
    text_file = open("high_score.txt","a+")
    text_file.write("{}".format(name))
    text_file.write("  {}\n".format(player.mission))
    #for i in range(N):
        #line = text_file.next().strip()
        #print line

    #print_text(screen, line, text_x, WIN_HEIGHT-250, 20, BLACK)
    
    text_file.close()
    
    pygame.display.flip()
    """


def end():
    pygame.quit()
    sys.exit()


def main():
    # Initialize variables and window
    pygame.init()
    global WIN_HEIGHT, WIN_WIDTH, HALF_WIDTH, HALF_HEIGHT
    end_screen = pygame.image.load('images/dead.png')
    bgimg = pygame.image.load('images/bg.png')
    heli = pygame.image.load("images/heli.png")
    total_level_width = bgimg.get_width()
    total_level_height = bgimg.get_height()
    level = 1

    info_object = pygame.display.Info()
    WIN_HEIGHT = info_object.current_h / 2 if (info_object.current_h / 2) < total_level_height else total_level_height
    WIN_WIDTH = info_object.current_w / 2 if (info_object.current_w / 2) < total_level_width else total_level_width
    HALF_WIDTH = int(WIN_WIDTH / 2)
    HALF_HEIGHT = int(WIN_HEIGHT / 2)

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FLAGS, DEPTH)
    pygame.display.set_caption("007 JAMES BOND")
    clock = pygame.time.Clock()

    name = show_intro(screen)
    james = Classes.JamesBond(total_level_width, total_level_height, name)

    while True:
        # Initialize objects
        james.rect.x, james.rect.y = animation_start_point

        all_sprites_list = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        flag_agents = 0
        obstacle_loc = []

        all_sprites_list.add(james)
        down = left = right = False

        camera = Classes.Camera(complex_camera, total_level_width, total_level_height)

        bg = Classes.Background(0, 0, bgimg)

        pygame.mouse.set_visible(0)

        add_trees(total_level_width, total_level_height, obstacle_loc, obstacles)
        add_coins(total_level_width, total_level_height, obstacle_loc, obstacles)

        start_animation(james, screen, all_sprites_list, clock, bgimg, level)
        screen.blit(bgimg, (0, 0))
        james.dress_to_ski()
        all_sprites_list.draw(screen)
        pygame.display.flip()

        while not james.dead:
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
            if james.rel_rect.y > animation_start_point[1] + 300 and flag_agents == 0:
                add_agents(total_level_width, obstacle_loc, obstacles)
                flag_agents = 1
            screen.blit(bgimg, (camera.apply(bg)))
            camera.update(james)
            james.update(down, left, right, camera, obstacles, level)
            show_points(screen, james)
            screen.blit(james.image, (camera.apply(james)))

            if james.rel_rect.y > int(total_level_height * 3.95 / 4):
                break

            for obstacle in obstacles:
                if isinstance(obstacle, Classes.Agent):
                    obstacle.track_player(james, level)

                if isinstance(obstacle, Classes.Coin):
                    obstacle.update_animation()

                screen.blit(obstacle.img, (camera.apply(obstacle)))
            pygame.display.update()

        if james.dead:
            # ends game in a terrible way...
            screen.blit(end_screen, (0, 0))
            score_sheet(screen, name, james)
            pygame.time.delay(1000)
            pygame.display.update()
            pygame.time.delay(4000)
            score_sheet(screen, name, james)
            pygame.display.update()
            end()

        theme1.fadeout(4000)
        heli_sound.play()
        heli_x, heli_y = WIN_WIDTH - WIN_WIDTH, WIN_HEIGHT - 200
        # for i in range(100):
        screen.blit(heli, (heli_x, heli_y))
        #    heli_x+=10
        #time.sleep(2)

        pygame.display.flip()
        pygame.display.update()
        screen.blit(escape, (0, 0))
        pygame.mouse.set_visible(1)
        pygame.time.delay(500)

        show_last_screen = True
        while show_last_screen:
            pygame.display.update()
            #pygame.time.delay(2000)
            score_sheet(screen, name, james)
            pygame.display.update()
            #continue
            #james.won = True
            #pygame.time.delay(5000)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    level += 1
                    james = Classes.JamesBond(total_level_width, total_level_height, name, james.power, james.lives,
                                              james.mission)
                    show_last_screen = False
                if event.type == QUIT:
                    end()


if __name__ == '__main__':
    main()
