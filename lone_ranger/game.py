#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from bullet import Bullet
from zombie import Zombie
from overlay import Overlay
from random import *

"""
Game Class
"""

class Game():

    def __init__(self):

        """
        ***Field Variables***
        self.engine
        self.sprites
        self.backgroundTiles
        self.foregroundTiles
        self.world_size
        self.player
        self.overlay
        self.numZombies
        self.zombies
        self.camera
        """

###############################################################################################################################################
        ##Create engine and initialize it
        self.engine = league.Engine("The Lone Ranger")
        self.engine.init_pygame()

        self.myBlocks = pygame.sprite.Group()

        #Setup the world
        self.sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
        self.backgroundTiles = league.Tilemap('./assets/background.lvl', self.sprites, layer = 0)
        self.foregroundTiles = league.Tilemap('./assets/world.lvl', self.sprites, layer = 1)
        self.world_size = (self.foregroundTiles.wide * league.Settings.tile_size, self.foregroundTiles.high * league.Settings.tile_size)
        self.engine.drawables.add(self.backgroundTiles.passable.sprites())
        self.engine.drawables.add(self.foregroundTiles.passable.sprites())
###############################################################################################################################################
        #self.bullets = []

        #Create the player character
        self.player = Player(self.engine, self.myBlocks, 3, 500, 400)
        self.player.blocks.add(self.foregroundTiles.impassable)
        self.player.world_size = self.world_size
        self.engine.objects.append(self.player)
        self.engine.drawables.add(self.player)

        #Player movements
        self.engine.key_events[pygame.K_w] = self.player.move_up
        self.engine.key_events[pygame.K_s] = self.player.move_down
        self.engine.key_events[pygame.K_a] = self.player.move_left
        self.engine.key_events[pygame.K_d] = self.player.move_right

        #Player shoot
        self.engine.key_events[pygame.K_SPACE] = self.player.shoot
###############################################################################################################################################
        #Create zombies
        self.numZombies = 0
        self.maxZombies = 100

        #Spawn zombies
        self.engine.events[pygame.USEREVENT + 0] = self.spawnZombie

        #Zombie spawn timer
        pygame.time.set_timer(pygame.USEREVENT + 0, 10000 // league.Settings.gameTimeFactor)
###############################################################################################################################################
        #Create bullets
###############################################################################################################################################
        #collisions
        #self.engine.collisions[self.zombies[0]] = (self.player, self.player.ouch)
###############################################################################################################################################
        #Create overlay
        self.overlay = Overlay(self.player)
        self.engine.objects.append(self.overlay)
        self.engine.drawables.add(self.overlay)
###############################################################################################################################################
        #Create camera that follows player
        self.camera = league.LessDumbCamera(800, 600, self.player, self.engine.drawables, self.world_size)
        self.engine.objects.append(self.camera)
###############################################################################################################################################
        #Sets up exit button to quit game
        self.engine.events[pygame.QUIT] = self.engine.stop
###############################################################################################################################################
        self.engine.run()

    def spawnZombie(self, time):
        if self.numZombies < self.maxZombies:
            randNumX = randint(10, 790)
            randNumY = randint(10, 790)

            zombie = Zombie(self.engine, self.myBlocks, self.player, 3, randNumX, randNumY)
            zombie.blocks.add(self.foregroundTiles.impassable)
            self.myBlocks.add(zombie)
            zombie.world_size = self.world_size
            self.engine.objects.append(zombie)
            self.engine.drawables.add(zombie)
            self.engine.objects.remove(self.camera)
            self.engine.objects.append(self.camera)

            self.numZombies += 1
        else:
            pass

    def main(self):
        self.game = Game()

if __name__ == '__main__':
    Game().main()
