from league import *
import pygame

class Bullet(Character):

    def __init__(self, direction, z = 0, x = 0, y = 0):

        super().__init__(z, x, y)

        
      
        self.direction = direction
        self.ttl = 0

        #A unit-less value. Bigger is faster.
        self.delta = 512

        # Where the bullets is fired from
        self.x = x
        self.y = y

        # The image to use. This will change frequently
        self.icon = [0,0,0,0,0,0,0,0]
        self.icon[0] = pygame.image.load('./assets/bullet.png').convert_alpha()
        self.icon[1] = pygame.transform.rotate(self.icon[0], 315).convert_alpha()
        self.icon[2] = pygame.transform.rotate(self.icon[0], 270).convert_alpha()
        self.icon[3] = pygame.transform.rotate(self.icon[0], 225).convert_alpha()
        self.icon[4] = pygame.transform.rotate(self.icon[0], 180).convert_alpha()
        self.icon[5] = pygame.transform.rotate(self.icon[0], 135).convert_alpha()
        self.icon[6] = pygame.transform.rotate(self.icon[0], 90).convert_alpha()
        self.icon[7] = pygame.transform.rotate(self.icon[0], 45).convert_alpha()
        self.icon[0] =  pygame.transform.rotate(self.icon[0], -45).convert_alpha()

        self.image = self.icon[direction]    

        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)

        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()

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

    def update(self, time):


        if time != 0:
            if self.direction == 0:
                self.y -= self.delta * time
            elif self.direction == 1:
                self.y -= (self.delta * time)/2
                self.x += (self.delta * time)/2
            elif self.direction == 2:
                self.x += self.delta * time
            elif self.direction == 3:
                self.x += (self.delta * time)/2
                self.y += (self.delta * time)/2
            elif self.direction == 4:
                self.y += (self.delta * time)
            elif self.direction == 5:
                self.x -= (self.delta * time)/2
                self.y += (self.delta * time)/2
            elif self.direction == 6:
                self.x -= (self.delta * time)
            elif self.direction == 7:
                self.x -= (self.delta * time)/2
                self.y -= (self.delta * time)/2


        self.rect.x = self.x
        self.rect.y = self.y

        #self.collisions = []

        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

        print(self.ttl)

        self.ttl += 1