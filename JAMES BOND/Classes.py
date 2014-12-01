import cmath
import random
from Constants import *


class JamesBond(pygame.sprite.Sprite):
    def __init__(self, width, height, power=game_default_power, lives=game_default_lives, mission=game_default_mission):
        super(JamesBond, self).__init__()
        self.power = power
        self.lives = lives
        self.mission = mission
        self.dead = False
        self.index_animation = 1
        self.image = animation_james_starting.convert_alpha()
        self.rect = self.image.get_rect()
        self.rel_rect = self.image.get_rect()
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

    def set_position_relative(self, x=None, y=None):
        if x is not None:
            self.rel_rect.x = x
        if y is not None:
            self.rel_rect.y = y

    def increase_position_relative(self, x=None, y=None):
        if x is not None:
            self.rel_rect.x += x
        if y is not None:
            self.rel_rect.y += y

    def get_position_screen(self):
        return [self.rect.x, self.rect.y]

    def get_position_relative(self):
        return [self.rel_rect.x, self.rel_rect.y]

    def update_animation(self):
        self.increase_position_screen(animation_step_x)
        self.index_animation = self.index_animation + 1 if self.index_animation < animation_number_sprites else 1
        image_name = animation_image_sprites.format(self.index_animation)
        self.image = pygame.image.load(image_name).convert_alpha()

    def dress_to_ski(self):
        self.increase_position_screen(animation_width_house)
        self.rel_rect = self.rect
        self.image = james_ski.convert_alpha()

    def update(self, down, left, right, camera, level):

        if down:
            self.image = james_down.convert_alpha()
            self.y = game_james_y_step * level
        if left:
            self.image = james_left.convert_alpha()
            self.x = -game_james_x_step
        if right:
            self.image = james_right.convert_alpha()
            self.x = game_james_x_step

        if self.get_position_relative()[0] + self.x < 0:
            self.set_position_relative(0)
        elif self.get_position_relative()[0] + self.x > self.level_width - self.image.get_width():
            self.set_position_relative(self.level_width - self.image.get_width())
        else:
            self.increase_position_relative(self.x)

        if self.get_position_relative()[1] + self.y > self.level_height - self.image.get_height():
            self.set_position_relative(y=self.level_height - self.image.get_height())
        else:
            self.increase_position_relative(y=self.y)

        self.rect = camera.apply(self)

    def collide(self, all_sprites_list):
        all_obstacles_collided = pygame.sprite.spritecollide(self, all_sprites_list, False)
        for obstacle in all_obstacles_collided:
            if isinstance(obstacle, Agent):
                agent_sound.play()
                if self.lives == 0:
                    self.dead = True
                else:
                    self.lives -= 1
                    self.power = game_default_power
                    self.rel_rect.top += game_agents_collide_top
                    obstacle.rel_rect.bottom -= game_agents_collide_james

            if isinstance(obstacle, Tree):
                tree_sound.play()
                if self.lives == 0:
                    self.dead = True
                if self.power == 0 and self.lives != 0:
                    self.lives -= 1
                    self.power = game_default_power
                else:
                    self.power -= 1
                self.rel_rect.bottom = obstacle.rel_rect.top
                return False

            if isinstance(obstacle, Coin):
                self.mission += game_coins_mission_power
                coin_sound.play()
                all_sprites_list.remove(obstacle)


class Background(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rel_rect = Rect(x, y, self.img.get_rect().size[0], self.img.get_rect().size[1])


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rel_rect = self.rect

    def update(self, camera):
        self.rect = camera.apply(self)

    @staticmethod
    def add(cls, number, min_row, max_row, min_col, max_col, obstacle_loc, all_sprites_list, number_row=1, step=0):
        for i in range(number):  # maps the obstacles
            row = random.randint(min_row, max_row)
            col = random.randint(min_col, max_col)
            for j in range(number_row):
                col += step
                location = [row, col]
                if not (location in obstacle_loc):  # makes sure two obstacles are not in the same location
                    obstacle_loc.append(location)
                    obj = cls(location[0], location[1])
                    all_sprites_list.add(obj)
                    all_sprites_list.add(obj)


class Tree(Obstacle):
    def __init__(self, x=0, y=0):
        super(Tree, self).__init__(x, y, game_tree_location_image)

    @classmethod
    def add(cls, total_level_width, total_level_height, *args):
        Obstacle.add(cls, game_trees_number, game_trees_min_row, total_level_width - game_trees_min_row,
                     animation_end_point[0], total_level_height - game_trees_max_col, *args)


class Agent(Obstacle):
    def __init__(self, x=0, y=0):
        self.dist = 0
        super(Agent, self).__init__(x, y, game_agents_location_image)

    def track_player(self, player, level):
        dx, dy = self.rel_rect.x - player.rel_rect.x, self.rel_rect.y - player.rel_rect.y
        self.dist = cmath.sqrt(dx * dx + dy * dy)
        dx, dy = float(dx / self.dist.real), float(dy / self.dist.real)
        self.rel_rect.x -= dx * 3
        self.rel_rect.y -= dy * 4 * level

    @classmethod
    def add(cls, total_level_width, *args):
        Obstacle.add(cls, game_agents_number, game_agents_min_row, total_level_width - game_agents_max_row,
                     animation_end_point[0] - game_agents_max_col, animation_end_point[0] + game_agents_max_col, *args)


class Coin(Obstacle):
    def __init__(self, x=0, y=0):
        self.angle = 1
        super(Coin, self).__init__(x, y, game_coins_location_image)
        self.image_set = []
        self.image_set.append(coin1.convert_alpha())
        self.image_set.append(coin2.convert_alpha())
        self.image_set.append(coin3.convert_alpha())
        self.image_set.append(coin4.convert_alpha())
        self.image_set.append(coin5.convert_alpha())
        self.image_set.append(coin6.convert_alpha())
        self.image_set.append(coin7.convert_alpha())
        self.image_set.append(coin8.convert_alpha())
        self.image_set.append(coin9.convert_alpha())
        self.image_set.append(coin10.convert_alpha())

    def update_animation(self):
        self.angle = self.angle + 1 if self.angle < 9 else 1
        self.image = self.image_set[self.angle]

    @classmethod
    def add(cls, total_level_width, total_level_height, *args):
        Obstacle.add(cls, game_coins_number, game_coins_min_row, total_level_width - game_coins_min_row,
                     animation_end_point[0], total_level_height - game_coins_max_col, number_row=game_coins_number_row,
                     step=game_coins_step, *args)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rel_rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rel_rect)
