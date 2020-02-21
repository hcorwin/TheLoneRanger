from league import *
import pygame
from bullet import Bullet

class Zombie(Character):

    """This is a sample class for a zombie object.  A zombie
    is a character, is a drawable, and an updateable object.
    This class should handle everything a zombie does, such as
    moving, attacking, collisions, etc.
    """

    def __init__(self, engine, myBlocks, player, z = 0, x = 0, y = 0):
        super().__init__(z, x, y)

        #############################################################################
        self.engine = engine
        self.type = "zombie"
        self.player = player
        #############################################################################

        # A unit-less value.  Bigger is faster.
        self.delta = 80

        # Where the zombie is positioned
        self.x = x
        self.y = y

        # The image to use. This will change frequently
        # in an animated Zombie class.
        self.image = pygame.image.load('./assets/zombie_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()

        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)

        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        self.myBlocks = myBlocks

        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []

        # For collision detection, we need to compare our sprite
        # with collideable sprites.  However, we have to remap
        # the collideable sprites coordinates since they change.
        # For performance reasons I created this sprite so we
        # don't have to create more memory each iteration of
        # collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

    def move_left(self, time):
        self.image = pygame.image.load('./assets/zombie_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []

        amount = self.delta * time
        self.x = self.x - amount
        self.update(0)

        while len(self.collisions) != 0:
            self.x = self.x + amount
            self.update(0)
            
    def move_left_up(self, time):
        self.image = pygame.image.load('./assets/zombie_left_up.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []

        amount = self.delta * time
        self.x = self.x - amount
        self.y = self.y - amount
        self.update(0)

        while len(self.collisions) != 0:
            self.x = self.x + amount
            self.y = self.y + amount
            self.update(0)
            
    def move_up(self, time):
        self.image = pygame.image.load('./assets/zombie_up.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []
    
        amount = self.delta * time
        self.y = self.y - amount
        self.update(0)

        while len(self.collisions) != 0:
            self.y = self.y + amount
            self.update(0)
            
    def move_right_up(self, time):
        self.image = pygame.image.load('./assets/zombie_right_up.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []
    
        amount = self.delta * time
        self.x = self.x + amount
        self.y = self.y - amount
        self.update(0)

        while len(self.collisions) != 0:
            self.x = self.x - amount
            self.y = self.y + amount
            self.update(0)

    def move_right(self, time):
        self.image = pygame.image.load('./assets/zombie_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []
        
        amount = self.delta * time
        self.x = self.x + amount
        self.update(0)

        while len(self.collisions) != 0:
            self.x = self.x - amount
            self.update(0)
            
    def move_right_down(self, time):
        self.image = pygame.image.load('./assets/zombie_right_down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []

        amount = self.delta * time
        self.x = self.x + amount
        self.y = self.y + amount
        self.update(0)

        while len(self.collisions) != 0:
            self.x = self.x - amount
            self.y = self.y - amount
            self.update(0)

    def move_down(self, time):
        self.image = pygame.image.load('./assets/zombie_down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []
        
        amount = self.delta * time
        self.y = self.y + amount
        self.update(0)

        while len(self.collisions) != 0:
            self.y = self.y - amount
            self.update(0)
            
    def move_left_down(self, time):
        self.image = pygame.image.load('./assets/zombie_left_down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []

        amount = self.delta * time
        self.x = self.x - amount
        self.y = self.y + amount
        self.update(0)

        while len(self.collisions) != 0:
            self.x = self.x + amount
            self.y = self.y - amount
            self.update(0)

    def update(self, time):
        if time != 0:
            self.move_towards_player(time)

        self.rect.x = self.x
        self.rect.y = self.y

        self.collisions = []

        for sprite in self.myBlocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collider):
                if type(sprite) is Bullet:
                    self.myBlocks.remove(self)
                    #self.engine.objects.remove(self)
                    self.engine.drawables.remove(self)
                    return
                else:
                    pass

        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)
                print("zombie collision with world object")

    def move_towards_player(self, time):

        if self.x > self.player.x and self.y == self.player.y:
            self.move_left(time)
        elif self.x < self.player.x and self.y == self.player.y:
            self.move_right(time)
        elif self.x == self.player.x and self.y > self.player.y:
            self.move_up(time)
        elif self.x == self.player.x and self.y < self.player.y:
            self.move_down(time)
        elif self.x > self.player.x and self.y > self.player.y:
            self.move_left_up(time)
        elif self.x > self.player.x and self.y < self.player.y:
            self.move_left_down(time)
        elif self.x < self.player.x and self.y > self.player.y:
            self.move_right_up(time)
        elif self.x < self.player.x and self.y < self.player.y:
            self.move_right_down(time)
        else:
            pass
