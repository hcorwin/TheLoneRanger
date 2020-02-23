from league import *
import pygame

class Player(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)
        # This unit's health
        self.health = 100
        #Length of time that can be sprinted
        self.sprintTime = 25
        #Time since last sprint
        self.sprintCooldown = 10
        #Can or cannot sprint
        self.canSprint = True
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 512
        # Where the player is positioned
        self.x = x
        self.y = y
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image = pygame.image.load('./assets/ranger_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []
        self.lives = 4
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
        self.overlay = self.font.render(str(self.health) + "        " + str(self.lives), True, (0,0,0))
        #player images
        self.icon = [0,0,0,0,0,0,0,0]
        self.icon[0] = pygame.image.load('./assets/ranger_up.png').convert_alpha()
        self.icon[1] = pygame.transform.rotate(self.icon[0], 315).convert_alpha()
        self.icon[2] = pygame.transform.rotate(self.icon[0], 270).convert_alpha()
        self.icon[3] = pygame.transform.rotate(self.icon[0], 225).convert_alpha()
        self.icon[4] = pygame.transform.rotate(self.icon[0], 180).convert_alpha()
        self.icon[5] = pygame.transform.rotate(self.icon[0], 135).convert_alpha()
        self.icon[6] = pygame.transform.rotate(self.icon[0], 90).convert_alpha()
        self.icon[7] = pygame.transform.rotate(self.icon[0], 45).convert_alpha()

        self.direction = 2

        #Wave the player is on 
        self.wave = 1
        #number of zomibes spawned in current wave
        self.zombieCount = 0
        self.lastShot = pygame.time.get_ticks()

    def updateSprite(self,keys):
        if keys[pygame.K_d]:
            if keys[pygame.K_w]:
                self.image = self.icon[1]
                self.direction = 1
            elif keys[pygame.K_s]: 
                self.image = self.icon[3]
                self.direction = 3
            else:
                self.image = self.icon[2]
                self.direction = 2

        elif keys[pygame.K_a]:
            if keys[pygame.K_w]:
                self.image = self.icon[7]
                self.direction = 7

            elif keys[pygame.K_s]: 
                self.image = self.icon[5]
                self.direction = 5

            else:
                self.image = self.icon[6]
                self.direction = 6

        elif keys[pygame.K_w]:
            self.image = self.icon[0]
            self.direction = 0
        elif keys[pygame.K_s]:
            self.image = self.icon[4]
            self.direction = 4
        self.image = pygame.transform.scale(self.image, (64, 64))
        
    def move(self, time, keys):
       

        amount = self.delta * time  
        
        if keys[pygame.K_LSHIFT] and self.sprintTime > 0 and self.canSprint:
            amount = amount * 1.5           
            self.sprintTime = self.sprintTime - 1
            if self.sprintCooldown > 0:
                self.sprintCooldown = self.sprintCooldown - 1
        
        if self.sprintTime < 25 and self.sprintCooldown == 10:
    
            self.sprintTime = self.sprintTime + 1
            if self.sprintTime > 10:
                self.canSprint = True
       
        if self.sprintCooldown < 10:
            if self.sprintCooldown == 0 and self.sprintTime == 0 and self.canSprint:
                self.canSprint = False 
            elif self.canSprint == False:
                self.sprintCooldown = self.sprintCooldown + 1  
        

        if (keys[pygame.K_a] and keys[pygame.K_s]) or (keys[pygame.K_a] and keys[pygame.K_w]):
            amount =  amount / 2

        if (keys[pygame.K_d] and keys[pygame.K_s]) or (keys[pygame.K_d] and keys[pygame.K_w]):
            amount =  amount / 2

        if keys[pygame.K_a]:
            try:
                if self.x - amount < 0:
                    raise OffScreenLeftExcepzombietion
                else:
                    self.x = self.x - amount
                    self.update(0)
                    while(len(self.collisions) != 0):
                       self.x = self.x + amount
                       self.update(0)
            except:
                pass
            
        
        if keys[pygame.K_d]:
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
            

        if keys[pygame.K_w]:
            try:
                if self.y - amount < 0:
                    raise OffScreenTopException
                else:
                    self.y = self.y - amount
                    self.update(0)
                    if len(self.collisions) != 0:
                        self.y = self.y + amount
                        self.update(0)
                        self.collisions = []
            except:
                pass
            
        if keys[pygame.K_s]:
            try:
                if self.y + amount > self.world_size[1] - Settings.tile_size:
                    raise OffScreenBottomException
                else:
                    self.y = self.y + amount
                    self.update(0)
                    if len(self.collisions) != 0:
                        self.y = self.y - amount
                        self.update(0)
                    self.collisions = []
            except:
                pass
          
        self.updateSprite(keys)
    

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []

        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now
        if self.health <= 0:
            self.health = 100
            self.lives = self.lives - 1
