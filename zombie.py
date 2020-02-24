from league import *
import pygame
import random
import math

class Zombie(Character):

    """This is a sample class for a zombie object.  A zombie
    is a character, is a drawable, and an updateable object.
    This class should handle everything a zombie does, such as
    moving, attacking, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    
    def __init__(self, player, z = 0, x = 0, y = 0):
    
        super().__init__(z, x, y)
        # This unit's health
        self.health = 100
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 125
        # Where the zombie is positioned
        self.x = x
        self.y = y
        # The image to use. This will change frequently
        # in an animated Zombie class.
        self.image = pygame.image.load('./assets/zombie_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = player.blocks
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
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf',32)
        #zombie sounds
        self.zombie_sound = sound
        self.zombie_sound.set_volume(0.3)
       
        
        #Zombie uses player object to find x y location on map and go after him
        self.player = player

        self.icon = [0,0,0,0,0,0,0,0]
        self.icon[0] = pygame.image.load('./assets/zombie_up.png').convert_alpha()
        self.icon[1] = pygame.transform.rotate(self.icon[0], 315).convert_alpha()
        self.icon[2] = pygame.transform.rotate(self.icon[0], 270).convert_alpha()
        self.icon[3] = pygame.transform.rotate(self.icon[0], 225).convert_alpha()
        self.icon[4] = pygame.transform.rotate(self.icon[0], 180).convert_alpha()
        self.icon[5] = pygame.transform.rotate(self.icon[0], 135).convert_alpha()
        self.icon[6] = pygame.transform.rotate(self.icon[0], 90).convert_alpha()
        self.icon[7] = pygame.transform.rotate(self.icon[0], 45).convert_alpha()
        self.icon[0] =  pygame.transform.rotate(self.icon[0], -45).convert_alpha()

        self.delta = 80
        self.shambleTimer = -999
        self.targetX = random.randint(-125,125) + self.player.x
        self.targetY = random.randint(-125,125) + self.player.y
    

    def move_left(self, time):

        self.image = self.icon[6]
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftExcepzombietion
            else:
                self.x = self.x - amount
                #self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    #self.update(0)
        except:
            pass
            
    def move_left_up(self, time):

        self.image = self.icon[7]
        self.image = pygame.transform.scale(self.image, (64, 64))
    
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            elif self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.x = self.x - amount
                self.y = self.y - amount
                #self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    self.y = self.y + amount
                 #   self.update(0)
        except:
            pass
            
    def move_up(self, time):

        self.image = self.icon[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
    
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                #self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    #self.update(0)
                    self.collisions = []
        except:
            pass
            
    def move_right_up(self, time):

        self.image = self.icon[0]
        self.image = pygame.transform.scale(self.image, (64, 64))
    
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            elif self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.x = self.x + amount
                self.y = self.y - amount
                #self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.y = self.y + amount
                 #   self.update(0)
        except:
            pass

    def move_right(self, time):

        self.image = self.icon[2]
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
              #  self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
               #     self.update(0)
        except:
            pass
            
    def move_right_down(self, time):

        self.image = self.icon[3]
        self.image = pygame.transform.scale(self.image, (64, 64))
    
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            elif self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.x = self.x + amount
                self.y = self.y + amount
               # self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.y = self.y - amount
                #    self.update(0)
        except:
            pass

    def move_down(self, time):

        self.image = self.icon[4]
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                #self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                  #  self.update(0)
                    self.collisions = []
        except:
            pass
            
    def move_left_down(self, time):
 # Could keep track of rectangles and update here, but eh.
        self.image = self.icon[5]
        self.image = pygame.transform.scale(self.image, (64, 64))
    
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            elif self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.x = self.x - amount
                self.y = self.y + amount
                #self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    self.y = self.y + amount
                   # self.update(0)
        except:
            pass

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        self.move_towards_player(time)
       
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 100
            self.last_hit = now
            self.zombie_sound.play()

    #function from https://community.esri.com/thread/158038 by user carlsunderman
    def calculateDistance(self,x1,y1,x2,y2):  
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return dist 

      

    def move_towards_player(self, time):
        # Find direction vector (dx, dy) between enemy and player.
        #dirvect = pygame.math.Vector2(self.x - self.player.x, self.y - self.player.y)
        
        #NOTE (0, 0) START IN TOP LEFT CORNER
        
        move = None
        now = pygame.time.get_ticks()
        if  now - self.shambleTimer > 250:
            #if (random.randint(0,100) > 25):
            if  self.calculateDistance(self.player.x, self.player.y, self.x, self.y) < 100:
                self.targetX = self.player.x 
                self.targetY = self.player.y 
            if  self.calculateDistance(self.player.x, self.player.y, self.x, self.y) > 100:
                self.targetX = self.player.x  +random.randint(-50,50)
                self.targetY = self.player.y  +random.randint(-50,50)

                self.shambleTimer = now
            if  self.calculateDistance(self.player.x, self.player.y, self.x, self.y) > 250:
                self.targetX = self.player.x +random.randint(-100,100)
                self.targetY = self.player.y +random.randint(-100,100)

                self.shambleTimer = now
            if  self.calculateDistance(self.player.x, self.player.y, self.x, self.y) >= 250:
                self.targetX = random.randint(-350,350) + self.player.x
                self.targetY = random.randint(-350,350) + self.player.y
                self.shambleTimer = now
            if  self.calculateDistance(self.player.x, self.player.y, self.x, self.y) > 1000:
                self.targetX = random.randint(-250,250) + self.x
                self.targetY = random.randint(-250,250) + self.y
                self.shambleTimer = now

        
        if self.x > self.targetX and self.y == self.targetY:
            self.move_left(time)
        elif self.x < self.targetX and self.y == self.targetY:
            self.move_right(time)
        elif self.x == self.targetX and self.y > self.targetY:
            self.move_up(time)
        elif self.x == self.targetX and self.y < self.targetY:
            self.move_down(time)
        elif self.x > self.targetX and self.y > self.targetY:
            self.move_left_up(time)
        elif self.x > self.targetX and self.y < self.targetY:
            self.move_left_down(time)
        elif self.x < self.targetX and self.y > self.targetY:
            self.move_right_up(time)
        elif self.x < self.targetX and self.y < self.targetY:
            self.move_right_down(time)
        else:
            pass
            
        
        
            
        
        
            
