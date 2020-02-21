from league import *
import pygame

class Bullet(Character):

    def __init__(self, engine, myBlocks, direction, z = 0, x = 0, y = 0):

        super().__init__(z, x, y)

        self.engine = engine
        self.myBlocks = myBlocks
        self.direction = direction
        self.ttl = 0

        #A unit-less value. Bigger is faster.
        self.delta = 512

        # Where the bullets is fired from
        self.x = x
        self.y = y

        # The image to use. This will change frequently
        if self.direction == "up":
            self.image = pygame.image.load('./assets/bullet_up.png').convert_alpha()
        elif self.direction == "down":
            self.image = pygame.image.load('./assets/bullet_down.png').convert_alpha()
        elif self.direction == "left":
            self.image = pygame.image.load('./assets/bullet_left.png').convert_alpha()
        else:
             self.image = pygame.image.load('./assets/bullet_right.png').convert_alpha()

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

    def ouch(self):
        print("HIT HIS ASS")

    def update(self, time):
        if self.ttl > 30:
            self.myBlocks.remove(self)
            self.engine.objects.remove(self)
            self.engine.drawables.remove(self)
            return


        if time != 0:
            if self.direction == "up":
                self.y -= self.delta * time
            elif self.direction == "down":
                self.y += self.delta * time
            elif self.direction == "left":
                self.x -= self.delta * time
            else:
                self.x += self.delta * time

        self.rect.x = self.x
        self.rect.y = self.y

        self.collisions = []

        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

        self.ttl += 1
