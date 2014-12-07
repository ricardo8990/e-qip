import cmath
import random
from Constants import *


class JamesBond(pygame.sprite.Sprite):
    def __init__(self, width, height, power=game_default_power, lives=game_default_lives, mission=game_default_mission):
        super(JamesBond, self).__init__()
        self.power = power  # james bond's health during one lifetime
        self.lives = lives  # james bond has three lives in a level
        self.mission = mission  # james bond's mission points, which increase as he collects coins/intelligence
        self.dead = False  # is james bond alive
        self.index_animation = 1  # james bond animation image index number
        self.image = animation_james_starting.convert_alpha()  # james bond image
        self.rect = self.image.get_rect()  # the following attributes help us keep track of james bond during the game
        self.x = self.rect.x
        self.y = self.rect.y
        self.level_width = width
        self.level_height = height

    def set_position_screen(self, x=None, y=None):
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y

    def increase_position_screen(self, x=None, y=None):
        if x is not None:
            self.rect.x += x
        if y is not None:
            self.rect.y += y

    def set_position_relative(self, x=None, y=None):  # sets james bond's position attributes
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y

    def increase_position_relative(self, x=None, y=None):  # increases james bond's position attributes
        if x is not None:
            self.rect.x += x
        if y is not None:
            self.rect.y += y

    def get_position_screen(self):
        return [self.rect.x, self.rect.y]

    def get_position_relative(self):  # gets james bond's position attributes
        return [self.rect.x, self.rect.y]

    def update_animation(self):
        # Increase the position, only in x
        self.increase_position_screen(animation_step_x)
        # Update the image
        self.index_animation = self.index_animation + 1 if self.index_animation < animation_number_sprites else 1
        image_name = animation_image_sprites.format(self.index_animation)
        self.image = pygame.image.load(image_name).convert_alpha()

    def dress_to_ski(self):
        self.increase_position_screen(animation_width_house)
        self.image = james_ski.convert_alpha()

    def update(self, down, left, right, level):  # updates james' position according to key presses

        if down:  # if down key is pressed
            self.image = james_down.convert_alpha()  # change bond image to skiing down
            self.y = game_james_y_step * level  # set speed
        if left:  # if left key is pressed
            self.image = james_left.convert_alpha()  # change bond image to skiing left
            self.x = -game_james_x_step  # set speed
        if right:  # if right key is pressed
            self.image = james_right.convert_alpha()  # change bond image to skiing right
            self.x = game_james_x_step  # set speed

        # out of bounds control for min x position
        if self.get_position_relative()[0] + self.x < 0:
            self.set_position_relative(0)
        # out of bounds control for max x position
        elif self.get_position_relative()[0] + self.x > self.level_width - self.image.get_width():
            self.set_position_relative(self.level_width - self.image.get_width())
        else:
            self.increase_position_relative(self.x)  # change position according to key press

        # out of bounds control for y position
        if self.get_position_relative()[1] + self.y > self.level_height - self.image.get_height():
            self.set_position_relative(y=self.level_height - self.image.get_height())
        else:
            self.increase_position_relative(y=self.y)  # change position according to key press

    def collide(self, all_sprites_list):  # collision detection for james bond
        all_obstacles_collided = pygame.sprite.spritecollide(self, all_sprites_list, False)  # get a list of collisions
        for obstacle in all_obstacles_collided:  # for all obstacles which have had collisions
            if isinstance(obstacle, Agent):  # if they are agents
                agent_sound.play()
                if self.lives == 0:  # the following determines the life/death/health attributes of james bond to loop
                    self.dead = True  # the game
                else:
                    self.lives -= 1  # agent collisions are fatal
                    self.power = game_default_power
                    self.rect.top += game_agents_collide_top  # we don't want a collision detection every clock tick
                    obstacle.rect.bottom -= game_agents_collide_james

            if isinstance(obstacle, Tree):  # if they are trees
                tree_sound.play()
                if self.lives == 0:  # determines the life/death/health attributes of james bond to loop the game
                    self.dead = True
                if self.power == 0 and self.lives != 0:
                    self.lives -= 1
                    self.power = game_default_power
                else:
                    self.power -= 1  # tree collisions decrease health value by 1
                self.rect.bottom = obstacle.rect.top  # james gets stuck
                return False

            if isinstance(obstacle, Coin):  # if they are coins/intelligence
                self.mission += game_coins_mission_power  # increase the mission point by 5
                coin_sound.play()
                all_sprites_list.remove(obstacle)  # remove the object


class Background(object):  # background
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = Rect(x, y, self.img.get_rect().size[0], self.img.get_rect().size[1])


class Obstacle(pygame.sprite.Sprite):  # obstacle
    def __init__(self, x, y, image_file):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.rect

    @staticmethod  # adds obstacles
    def add(cls, number, min_row, max_row, min_col, max_col, obstacle_loc, all_sprites_list, number_row=1, step=0):
        for i in range(number):  # maps the designated number of obstacles
            row = random.randint(min_row, max_row)  # randomly
            col = random.randint(min_col, max_col)
            for j in range(number_row):
                col += step  # step number is the distance between to objects.  This is 0 by default.
                # But 30 for coins, because they are placed consecutively and we don't want them to overlap.
                location = [row, col]
                if not (location in obstacle_loc):  # makes sure two obstacles are not in the same location
                    obstacle_loc.append(location)  # holds the list of obstacle locations that have been placed
                    obj = cls(location[0], location[1])  # create obstacle object
                    all_sprites_list.add(obj)  # put it in the permanent list


class Tree(Obstacle):  # trees
    def __init__(self, x=0, y=0):
        super(Tree, self).__init__(x, y, game_tree_location_image)

    @classmethod
    def add(cls, total_level_width, total_level_height, *args):
        Obstacle.add(cls, game_trees_number, game_trees_min_row, total_level_width - game_trees_min_row,
                     animation_end_point[0], total_level_height - game_trees_max_col, *args)


class Agent(Obstacle):  # enemy agent
    def __init__(self, x=0, y=0):
        self.dist = 0  # distance between enemy agent and james bond
        super(Agent, self).__init__(x, y, game_agents_location_image)

    def track_player(self, player, level):  # tracking james bond
        # defines the x and y distances between agent and james bond
        dx, dy = self.rect.x - player.rect.x, self.rect.y - player.rect.y
        self.dist = cmath.sqrt(dx * dx + dy * dy)  # this is the absolute distance
        if self.dist == 0:
            return
        dx, dy = float(dx / self.dist.real), float(
            dy / self.dist.real)  # determine the direction that agent is going to travel on
        self.rect.x -= dx * 3  # add some speed
        self.rect.y -= dy * 4 * level  # add some speed, increases each level. agents travel faster in y direction

    @classmethod
    def add(cls, total_level_width, *args):  # add agent
        Obstacle.add(cls, game_agents_number, game_agents_min_row, total_level_width - game_agents_max_row,
                     animation_end_point[0] - game_agents_max_col, animation_end_point[0] + game_agents_max_col, *args)


class Coin(Obstacle):  # coins/intelligence
    def __init__(self, x=0, y=0):
        self.angle = 1
        super(Coin, self).__init__(x, y, game_coins_location_image)
        self.image_set = []  # holds the preloaded image set
        self.image_set.append(coin1.convert_alpha())  # all are images of different angles of the coin object
        self.image_set.append(coin2.convert_alpha())
        self.image_set.append(coin3.convert_alpha())
        self.image_set.append(coin4.convert_alpha())
        self.image_set.append(coin5.convert_alpha())
        self.image_set.append(coin6.convert_alpha())
        self.image_set.append(coin7.convert_alpha())
        self.image_set.append(coin8.convert_alpha())
        self.image_set.append(coin9.convert_alpha())
        self.image_set.append(coin10.convert_alpha())

    def update_animation(self):  # the revolution around axis animation for coins
        self.angle = self.angle + 1 if self.angle < 9 else 1  # a different angle is displayed with every clock tick
        self.image = self.image_set[self.angle]

    @classmethod
    def add(cls, total_level_width, total_level_height, *args):  # add coins
        Obstacle.add(cls, game_coins_number, game_coins_min_row, total_level_width - game_coins_min_row,
                     animation_end_point[0], total_level_height - game_coins_max_col, number_row=game_coins_number_row,
                     step=game_coins_step, *args)


# Helps follow james bond on the screen as he skies down.
class Camera(object):  # camera
    def __init__(self, tracker_func, width, height):
        self.tracker_func = tracker_func
        self.rect_pos = Rect(0, 0, width, height)  # starting position is 0,0 and the width and height of the window

    # target is moved by the given offset, which is the camera's top-left position
    def apply(self, target):
        return target.rect.move(self.rect_pos.topleft)

    # changes the camera position, according to target's values which will be james bond
    def update(self, target):
        self.rect_pos = self.tracker_func(self.rect_pos, target.rect)