import Classes
import sys
from Constants import *


def game_camera(camera, target_rect):  #center james bond in the middle, camera tracking function
    #defines a rectangle as follows:
    l, t, _, _ = target_rect  #left and top values of the target rectangle 
    _, _, w, h = camera  #width and height of the camera
    l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h  #the new rectangle positions james bond in the middle

    l = min(0, l)  #out of bounds checks for x
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)  #out of bounds checks y
    t = min(0, t)
    return Rect(l, t, w, h)  #return the new rectangle


def print_text(screen, text, x, y, size, colour): #displays text onto the screen 
    game_font = pygame.font.Font(None, size)
    text_render = game_font.render(text, 1, colour)
    text_rect = text_render.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text_render, text_rect)


def show_points(screen, player): # prints the player name,points,power on the screen 
    first_line_text = game_default_points_text1.format(player.power)
    second_line_text = game_default_points_text2.format(player.lives)
    third_line_text = game_default_points_text3.format(player.mission)
    print_text(screen, first_line_text, 0, 70, 15, pygame.color.THECOLORS["black"])
    print_text(screen, second_line_text, 0, 80, 15, pygame.color.THECOLORS["black"])
    print_text(screen, third_line_text, 0, 90, 15, pygame.color.THECOLORS["black"])


def start_animation(james, screen, all_sprites_list, clock, bgimg, level):  
    r = animation_letter_size
    while james.rect.x <= animation_end_point[0]: 
        screen.blit(bgimg, (0, 0))
        james.update_animation()
        for c in [s for s in all_sprites_list.spritedict if isinstance(s, Classes.Coin)]: 
            c.update_animation()
        text = animation_text.format(level)
        all_sprites_list.draw(screen)
        print_text(screen, text, HALF_WIDTH - len(text), HALF_HEIGHT, r, pygame.color.THECOLORS["black"])
        clock.tick(20)
        pygame.display.flip()
        r -= 1


def show_intro(screen): #displays the Home screen
    theme1.play(-1) 
    first_screen = title_screen
    text_y = int(9 * WIN_HEIGHT / 10)
    name = ""
    completed = False

    while not completed:
        screen.fill(pygame.color.THECOLORS["white"])
        screen.blit(first_screen, (0, 0))    
        print_text(screen, intro_text1, intro_text_x, text_y, 30, pygame.color.THECOLORS["black"])
        if name != "":
            print_text(screen, intro_text2, intro_text_x, WIN_HEIGHT - 20, 20, pygame.color.THECOLORS["black"])
        for evt in pygame.event.get():  # get user input for name and Enter
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN and name != "":
                    completed = True
            elif evt.type == QUIT:
                end()
        print_text(screen, name, 100, text_y, 30, pygame.color.THECOLORS["black"])
        pygame.display.flip()

    pygame.mixer.pause()
    return name  


def score_sheet(screen, name, player):
    #writes the name and score in the text file
    write_file = open(game_default_score_sheet_file, "a")
    write_file.write("{},{}\n".format(name, player.mission))
    write_file.close()

    #reads the line and puts in a list
    read_file = open(game_default_score_sheet_file, "r")
    scores=[]
    for line in read_file:
        x = line.split(",")
        a = x[0]
        b = int(x[1])
        scores.append((b,a))
    read_file.close()
    scores.sort()
    scores.reverse()   # sorted scores available in list  
    
    count = 0
    text_y = game_default_score_text_y

    for i in scores:     # prints the top 5 scores onto the screen using print_text func
        t_width = 40
        for z in range(2):
            #prints the score onto the screen 
            print_text(screen, str(i[z]), t_width, text_y, game_default_score_text_size,
                       pygame.color.THECOLORS["black"])
            t_width += 80
        count += 1
        if count >= 5:
            break
        text_y += 20



def end():   # func to exit the game
    pygame.quit()
    sys.exit()


def main():
    global WIN_HEIGHT, WIN_WIDTH, HALF_WIDTH, HALF_HEIGHT
    pygame.init()

    # Initialize window
    total_level_width = bgimg.get_width()
    total_level_height = bgimg.get_height()
    level = 1  #start at level 1
    info_object = pygame.display.Info()
    #window width and height are hardware independent
    WIN_HEIGHT = int(info_object.current_h * WINDOW_HEIGHT_PERCENTAGE) \
        if (info_object.current_h * WINDOW_HEIGHT_PERCENTAGE) < total_level_height else total_level_height
    WIN_WIDTH = int(info_object.current_w * WINDOW_WIDTH_PERCENTAGE) \
        if (info_object.current_w * WINDOW_WIDTH_PERCENTAGE) < total_level_width else total_level_width
    HALF_WIDTH = int(WIN_WIDTH / 2)  #half width
    HALF_HEIGHT = int(WIN_HEIGHT / 2) #half height
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FLAGS, DEPTH)  #create screen
    pygame.display.set_caption(WINDOW_TITLE)  #set caption
    clock = pygame.time.Clock()  #clock
    

    # Show the intro
    name = show_intro(screen)
    # Create James
    james = Classes.JamesBond(total_level_width, total_level_height)

    while True:
        # Initialize objects, variables and sprites
        all_sprites_list = pygame.sprite.Group()  #holds the list of all sprites
        all_sprites_list.add(james)  #add james bond to all_sprites list
        flag_agents = True #no agents at the start of the game
        obstacle_loc = []  #list that holds all obstacle locations
        down = left = right = False
        camera = Classes.Camera(game_camera, total_level_width, total_level_height)  #create camera object
        bg = Classes.Background(0, 0, bgimg)  #create background object

        Classes.Tree.add(total_level_width, total_level_height, obstacle_loc, all_sprites_list)  #add trees
        Classes.Coin.add(total_level_width, total_level_height, obstacle_loc, all_sprites_list)  #add coins/intelligence

        #Reproduce the sounds
        bond_voice.play()
        main_theme.play(-1)

        james.set_position_screen(animation_start_point[0], animation_start_point[1])  #place james at correct position for the start animation
        start_animation(james, screen, all_sprites_list, clock, bgimg, level)  #start the animation

        screen.blit(bgimg, (0, 0))
        james.dress_to_ski()  #james bond changes clothes
        #all_sprites_list.draw(screen)
        pygame.display.flip()

        while not james.dead:
            clock.tick(60)

            # Check the events for right, left and down arrow
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    end()
                elif evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_LEFT:
                        left = True
                    elif evt.key == pygame.K_RIGHT:
                        right = True
                    elif evt.key == pygame.K_DOWN:
                        down = True
                elif evt.type == pygame.KEYUP:
                    if evt.key == pygame.K_LEFT:
                        left = False
                    elif evt.key == pygame.K_RIGHT:
                        right = False
                    elif evt.key == pygame.K_DOWN:
                        down = False

            #If james has advanced more than game_agents_start_y we create the agents
            if james.get_position_relative()[1] > animation_start_point[1] + game_agents_start_y and flag_agents:
                Classes.Agent.add(total_level_width, obstacle_loc, all_sprites_list)
                flag_agents = False

            #Update the background, the camera and James
            screen.blit(bgimg, (camera.apply(bg)))
            camera.update(james)  #change camera position according to james
            james.update(down, left, right, camera, level)  #james moves according to key presses
            #Detect if James has collided with something
            james.collide(all_sprites_list)

            #Update the obstacles according to their types, agents have to track James and coins must revolve around their axis
            for obstacle in all_sprites_list:
                if isinstance(obstacle, Classes.Agent):
                    obstacle.track_player(james, level)

                if isinstance(obstacle, Classes.Coin):
                    obstacle.update_animation()
                #if not isinstance(obstacle,Classes.JamesBond):
                    #obstacle.update(camera)
                screen.blit(obstacle.image,camera.apply(obstacle))

            #Draw all the elements in the screen
            show_points(screen, james)
            #all_sprites_list.draw(screen)
            pygame.display.update()

            #If James has reached the limit in the edge y, we finish the level
            if james.rect.y > int(total_level_height * game_default_end_game_portion):
                break

        #when james is dead shows final screen with Score list
        if james.dead:
            shot_sound.play()
            screen.blit(end_screen, (0, 0))
            score_sheet(screen, name, james)
            pygame.display.update()
        else:
            #when james escapes, flight appears end screen is shown
            heli_sound.play()
            screen.blit(heli, (0, WIN_HEIGHT - 200))
            pygame.display.flip()
            pygame.time.delay(500)
            screen.fill(pygame.color.THECOLORS["white"])
            screen.blit(escape, (0, 0))
            
            
            pygame.display.update()

        show_last_screen = True
        main_theme.fadeout(1000)
        
        while show_last_screen:
            #detects keyboard input, JamesBond is called again to restart the game
            for evt in pygame.event.get():
                if evt.type == KEYDOWN and evt.key == K_RETURN:
                    if james.dead:
                        level = 1
                        james = Classes.JamesBond(total_level_width, total_level_height)
                    else:
                        level += 1
                        james = Classes.JamesBond(total_level_width, total_level_height, james.power, james.lives,
                                                  james.mission)
                    show_last_screen = False
                if evt.type == QUIT:
                    end()


if __name__ == '__main__':
    main()
