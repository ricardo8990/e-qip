import pygame
from pygame import *

#Window configuration
WIN_HEIGHT = 800
WIN_WIDTH = 868
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DEPTH = 32
FLAGS = 0
WINDOW_HEIGHT_PERCENTAGE = 0.75
WINDOW_WIDTH_PERCENTAGE = 0.5
WINDOW_TITLE = "007 JAMES BOND"

#Images
end_screen = pygame.image.load('images/dead.png')
bgimg = pygame.image.load('images/bg2.png')
heli = pygame.image.load("images/heli.png")
title_screen = pygame.image.load('images/scr3.jpg')
escape = pygame.image.load('images/esc.png')
james_ski = pygame.image.load('images/bond skiing.png')
james_down = pygame.image.load('images/bond skiing.png')
james_left = pygame.image.load("images/ski left.png")
james_right = pygame.image.load("images/ski right.png")
coin1 = pygame.image.load("images/coin1.png")
coin2 = pygame.image.load("images/coin2.png")
coin3 = pygame.image.load("images/coin3.png")
coin4 = pygame.image.load("images/coin4.png")
coin5 = pygame.image.load("images/coin5.png")
coin6 = pygame.image.load("images/coin6.png")
coin7 = pygame.image.load("images/coin7.png")
coin8 = pygame.image.load("images/coin8.png")
coin9 = pygame.image.load("images/coin9.png")
coin10 = pygame.image.load("images/coin10.png")

#Sound
pygame.mixer.init(22050, -16, 2, 2096)
theme1 = pygame.mixer.Sound("sounds/bond.wav")
heli_sound = pygame.mixer.Sound("sounds/Heli.wav")
main_theme = pygame.mixer.Sound("sounds/main_theme.wav")
bond_voice = pygame.mixer.Sound("sounds/sc_bond.wav")
coin_sound = pygame.mixer.Sound("sounds/coin.aiff")
tree_sound = pygame.mixer.Sound("sounds/tree.wav")
agent_sound = pygame.mixer.Sound("sounds/agent.wav")
shot_sound = pygame.mixer.Sound("sounds/shot.wav")

#Configuration for intro
intro_text_x = 30
intro_text1 = "Name: "
intro_text2 = "Enter to continue..."

#Configuration for initial animation
animation_start_point = (0, 90)
animation_end_point = (208, 90)
animation_james_starting = pygame.image.load("images/jamesr1.png")
animation_letter_size = 70
animation_text = "LEVEL {}"
animation_step_x = 3
animation_number_sprites = 8
animation_image_sprites = "images/jamesr{}.png"
animation_width_house = 45

#Configuration for the game
game_tree_location_image = "images/tree.png"
game_trees_number = 30
game_trees_min_row = 30
game_trees_max_col = 120
game_coins_location_image = "images/coin1.png"
game_coins_number = 10
game_coins_min_row = 50
game_coins_max_col = 300
game_coins_number_row = 4
game_coins_step = 30
game_coins_mission_power = 5
game_agents_location_image = "images/agent_skiing.png"
game_agents_start_y = 300
game_agents_number = 1
game_agents_min_row = 10
game_agents_max_row = 30
game_agents_max_col = 50
game_agents_collide_top = 20
game_agents_collide_james = 50
game_james_y_step = 3.9
game_james_x_step = 3
game_default_lives = 3
game_default_power = 100
game_default_mission = 0
game_default_end_game_portion = 3.95 / 4
game_default_score_sheet_file = "high_score.txt"
game_default_score_text_y = 250
game_default_score_text_size = 25
game_default_points_text1 = "Health: {}"
game_default_points_text2 = "Lives: {}"
game_default_points_text3 = "Mission: {}"
game_default_text_size = 15