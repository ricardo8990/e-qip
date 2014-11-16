import pygame


# ----------------------------------------------------#
#               Class definitions                    #
#----------------------------------------------------#
class JamesBond(pygame.sprite.Sprite):
    def __init__(self):
        super(JamesBond, self).__init__()
        self.index = 1
        self.image = pygame.image.load("images/jamesr1.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 3
        self.index = self.index + 1 if self.index < 8 else 1
        image_name = "images/jamesr{}.png".format(self.index)
        self.image = pygame.image.load(image_name).convert_alpha()

#----------------------------------------------------#
#               Initialize animation                 #
#----------------------------------------------------#
#Initialize pygame
pygame.init()
#Set the settings for the screen
infoObject = pygame.display.Info()
width = infoObject.current_w / 2
height = infoObject.current_h / 2
windowSize = (width, height)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("007 JAMES BOND")

#Used for manage how fast is the screen updated
clock = pygame.time.Clock()

#Variable for finish the animation
done = False

startingPoint = width / 8
endPoint = width / 2
james = JamesBond()
james.rect.x = startingPoint
james.rect.y = height / 8

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(james)

while james.rect.x <= endPoint:
    #Cleen the scene
    screen.fill(pygame.color.THECOLORS["green"])
    james.update()
    all_sprites_list.draw(screen)
    clock.tick(20)
    pygame.display.flip()
    startingPoint = james.rect.x