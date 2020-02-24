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
        # Length of time that can be sprinted
        self.sprintTime = 25
        # Time since last sprint
        self.sprintCooldown = 10
        # Can or cannot sprint
        self.canSprint = True
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 275
        # Where the player is positioned
        self.x = x
        self.y = y
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []
        self.lives = 4
        #Having to do with animation
        self.step_count = 0
        self.images = {}
        self.direction = Direction.EAST
        self.state = State.IDLE
        self.state_time = pygame.time.get_ticks()
        self.images[State.MOVE] = self.load_images("./assets/survivor-move_rifle_0")
        self.image = self.images[State.MOVE][Direction.EAST][0]
        self.frame = 0
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
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.overlay = self.font.render(str(self.health) + "        " + str(self.lives), True, (0, 0, 0))

        self.direction = 2

        # Wave the player is on
        self.wave = 1

        #number of kill
        self.kills = 0
        # number of zomibes spawned in current wave
        self.zombieCount = 0
        self.lastShot = pygame.time.get_ticks()
    def update_image(self):
        if self.state != State.MOVE:
            self.image = self.images[self.state][self.direction][self.frame % 10]
        else:
            self.image = self.images[self.state][self.direction][self.step_count]

    def updateSprite(self, keys):
        if keys[pygame.K_d]:
            if keys[pygame.K_w]:
                self.switch_state(State.MOVE)
                if self.direction != Direction.NORTHEAST:
                    self.switch_dir(Direction.NORTHEAST)
                else:
                    self.step_count = (self.step_count + 1) % 10
                self.update_image()
            elif keys[pygame.K_s]:
                self.switch_state(State.MOVE)
                if self.direction != Direction.SOUTHEAST:
                    self.switch_dir(Direction.SOUTHEAST)
                else:
                    self.step_count = (self.step_count + 1) % 10
                self.update_image()
            else:
                self.switch_state(State.MOVE)
                if self.direction != Direction.EAST:
                    self.switch_dir(Direction.EAST)
                else:
                    self.step_count = (self.step_count + 1) % 10
                self.update_image()

        elif keys[pygame.K_a]:
            if keys[pygame.K_w]:
                self.switch_state(State.MOVE)
                if self.direction != Direction.NORTHWEST:
                    self.switch_dir(Direction.NORTHWEST)
                else:
                    self.step_count = (self.step_count + 1) % 10
                self.update_image()

            elif keys[pygame.K_s]:
                self.switch_state(State.MOVE)
                if self.direction != Direction.SOUTHWEST:
                    self.switch_dir(Direction.SOUTHWEST)
                else:
                    self.step_count = (self.step_count + 1) % 10
                self.update_image()

            else:
                self.switch_state(State.MOVE)
                if self.direction != Direction.WEST:
                    self.switch_dir(Direction.WEST)
                else:
                    self.step_count = (self.step_count + 1) % 10
                self.update_image()

        elif keys[pygame.K_w]:
            self.switch_state(State.MOVE)
            if self.direction != Direction.NORTH:
                self.switch_dir(Direction.NORTH)
            else:
                self.step_count = (self.step_count + 1) % 10
            self.update_image()
        elif keys[pygame.K_s]:
            self.switch_state(State.MOVE)
            if self.direction != Direction.SOUTH:
                self.switch_dir(Direction.SOUTH)
            else:
                self.step_count = (self.step_count + 1) % 10
            self.update_image()

    def move(self, time, keys):

        amount = self.delta * time

        if keys[pygame.K_LSHIFT] and self.sprintTime > 0 and self.canSprint:
            amount = amount * 1.65
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
            amount = amount / 2

        if (keys[pygame.K_d] and keys[pygame.K_s]) or (keys[pygame.K_d] and keys[pygame.K_w]):
            amount = amount / 2

        if keys[pygame.K_a]:
            try:
                if self.x - amount < 0:
                    raise OffScreenLeftException
                else:
                    self.x = self.x - amount
                    self.update(0)
                    while (len(self.collisions) != 0):
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
                    while (len(self.collisions) != 0):
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

        self.frame = (self.frame + 1) % Settings.fps
        self.image = self.images[self.state][self.direction][self.frame % 10]

        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def switch_state(self, state):
        time = pygame.time.get_ticks()
        if self.state != state:
            self.state = state
            self.state_time = time

    def switch_dir(self, direction):
        self.direction = direction
        self.step_count = 0

    def load_images(self, path):
        images = {}
        right = {}
        left = {}
        up = {}
        down = {}
        upright = {}
        upleft = {}
        downleft = {}
        downright = {}

        for i in range(0, 20):
            p = path + str(i) + ".png"
            temp = pygame.image.load(p).convert_alpha()
            temp = pygame.transform.scale(temp, (64, 64))
            right[i] = temp
            left[i] = pygame.transform.flip(temp, True, False)
            up[i] = pygame.transform.rotate(temp, 90)
            down[i] = pygame.transform.rotate(temp, 270)
            upleft[i] = pygame.transform.rotate(temp, 135)
            upright[i] = pygame.transform.rotate(temp, 45)
            downleft[i] = pygame.transform.rotate(temp, 225)
            downright[i] = pygame.transform.rotate(temp, 315)
        images[Direction.EAST] = right
        images[Direction.WEST] = left
        images[Direction.NORTH] = up
        images[Direction.SOUTH] = down
        images[Direction.NORTHEAST] = upright
        images[Direction.NORTHWEST] = upleft
        images[Direction.SOUTHWEST] = downleft
        images[Direction.SOUTHEAST] = downright
        return images


    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now
        if self.health <= 0:
            self.health = 100
            self.lives = self.lives - 1
