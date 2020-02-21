from league import *
import pygame
from bullet import Bullet
from zombie import Zombie

class Player(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc. It was hastily
    written as a demo but should direction.
    """
    def __init__(self, engine, myBlocks, z = 0, x = 0, y = 0):
        super().__init__(z, x, y)

        #############################################################################
        self.type = "player"
        self.engine = engine
        self.direction = None
        self.kills = 0
        #############################################################################
        
        #Player health
        self.health = 100

        #Player lives
        self.lives = 4

        #Last time player was hurt
        self.last_hit = pygame.time.get_ticks()

        #Last time player shot
        self.last_shoot = pygame.time.get_ticks()

        #A unit-less value. Bigger is faster.
        self.delta = 256

        #Where the player is positioned
        self.x = x
        self.y = y

        #The image to use. This will change frequently in an animated Player class.
        self.image = pygame.image.load('./assets/ranger_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        #How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)

        #What sprites am I not allowed to cross?
        self.blocks = pygame.sprite.Group()
        self.myBlocks = myBlocks

        #Uses circle to detect collisions calls function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []

        #For collision detection, we need to compare our sprite
        #with collideable sprites.  However, we have to remap
        #the collideable sprites coordinates since they change.
        #For performance reasons I created this sprite so we
        #don't have to create more memory each iteration of
        #collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

    def move_up(self, time):

        self.direction = "up"
        self.image = pygame.image.load('./assets/ranger_up.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []

        amount = self.delta * time
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.update(0)
        except:
            pass

    def move_down(self, time):

        self.direction = "down"
        self.image = pygame.image.load('./assets/ranger_down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []

        amount = self.delta * time
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
        except:
            pass

    def move_left(self, time):

        self.direction = "left"
        self.image = pygame.image.load('./assets/ranger_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.collisions = []
        
        amount = self.delta * time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    self.update(0)
        except:
            pass

    def move_right(self, time):

        self.direction = "right"
        self.image = pygame.image.load('./assets/ranger_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
    
        self.collisions = []

        amount = self.delta * time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.update(0)
        except:
            pass

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now

    def shoot(self, time):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > 500:
            bullet = Bullet(self.engine, self.myBlocks, self.direction, 3, self.rect.x, self.rect.y)
            self.myBlocks.add(bullet)
            self.engine.objects.append(bullet)
            self.engine.drawables.add(bullet)
            self.last_shoot = now

    def update(self, time):
        if self.health < 0:
            self.lives -= 1
            self.health = 100

        #if self.lives < 0:

        self.rect.x = self.x
        self.rect.y = self.y

        self.collisions = []

        for sprite in self.myBlocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collider):
                if type(sprite) is Zombie:
                    self.ouch()
                elif sprite is Bullet:
                    pass
                else:
                    pass

        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)
                print("collision with world object")
