import pygame, sys, math, random, Classes
from pygame import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

bond = 'images/bond skiing.png'
e1 = 'images/e1.jif'
theme1 = pygame.mixer.Sound("bond.wav")
title_screen = 'images/scr3.jpg'
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


def end():
    pygame.quit()
    sys.exit()


def print_text(screen, text, x, y, size, colour):
    game_font = pygame.font.Font(None, size)
    text_render = game_font.render(text, 1, colour)
    text_rect = text_render.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text_render, text_rect)


def show_points(screen, player):
    first_line_text = "Points: %d" % player.points
    second_line_text = "Lives: %d" % player.lives
    print_text(screen, player.name, 0, 60, 15, BLACK)
    print_text(screen, first_line_text, 0, 70, 15, BLACK)
    print_text(screen, second_line_text, 0, 80, 15, BLACK)


def show_intro(screen):
    theme1.play(-1)
    first_screen = pygame.image.load(title_screen)
    text_x = 30
    text_y = int(9*WIN_HEIGHT / 10)
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


def main():
    # Initialize variables and window
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

    name = show_intro(screen)

    #Initialize objects
    james = Classes.JamesBond(total_level_width, total_level_height, name)
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
    chance_to_appear = 0.04

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

        if james.isPlaying:
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
        show_points(screen, james)
        all_sprites_list.draw(screen)
        camera.apply(james)
        pygame.display.update()


if __name__ == '__main__':
    main()
