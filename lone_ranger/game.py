#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from zombie import Zombie
from overlay import Overlay
from random import *

"""
Game Class
"""

class Game():

    def __init__(self):
    
        self.engine = None
        self.sprites = None
        self.backgroundTiles = None
        self.foregroundTiles = None
        self.world_size = None
        self.player = None
        self.overlay = None
        self.numZombies = None
        self.zombies = None
        self.camera = None
        
        #Create engine
        engine = league.Engine("The Lone Ranger")
        engine.init_pygame()
        
        #Setup the world
        sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
        backgroundTiles = league.Tilemap('./assets/background.lvl', sprites, layer = 0)
        foregroundTiles = league.Tilemap('./assets/world.lvl', sprites, layer = 1)
        world_size = (foregroundTiles.wide * league.Settings.tile_size, foregroundTiles.high * league.Settings.tile_size)
        engine.drawables.add(backgroundTiles.passable.sprites())
        engine.drawables.add(foregroundTiles.passable.sprites())
        
        #Create player object
        player = Player(2, 400, 300)
        player.blocks.add(foregroundTiles.impassable)
        player.world_size = world_size
        player.rect = player.image.get_rect()
        engine.objects.append(player)
        engine.drawables.add(player)
        
        #Create overlay
        overlay = Overlay(player)
        engine.objects.append(overlay)
        engine.drawables.add(overlay)
        
        #Create zombies
        numZombies = 4
        
        zombies = []
        randNum = 0
        
        for zombie in range(0, numZombies):
            zombies.append(Zombie(player, 10, 100 + randNum, 500 + randNum))
            engine.objects.append(zombies[zombie])
            engine.drawables.add(zombies[zombie])
            randNum = randint(1, 400)
        
        #Create camera that follows player
        camera = league.LessDumbCamera(800, 600, player, engine.drawables, world_size)
        engine.objects.append(camera)
        engine.objects.append(camera)
        
        engine.collisions[player] = (zombies[0], player.ouch)
        #need to register more collisions with new zombie here
        
        #Register events?
        pygame.time.set_timer(pygame.USEREVENT + 0, 1000 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000 // league.Settings.gameTimeFactor)
        pygame.time.set_timer(pygame.USEREVENT + 3, 1000 // league.Settings.gameTimeFactor)
        
        #Player movements
        engine.key_events[pygame.K_a] = player.move_left
        engine.key_events[pygame.K_d] = player.move_right
        engine.key_events[pygame.K_w] = player.move_up
        engine.key_events[pygame.K_s] = player.move_down
        
        #Register zombie movements in event list
        engine.events[pygame.USEREVENT + 0] = zombies[0].move_towards_player
        engine.events[pygame.USEREVENT + 1] = zombies[1].move_towards_player
        engine.events[pygame.USEREVENT + 2] = zombies[2].move_towards_player
        engine.events[pygame.USEREVENT + 3] = zombies[3].move_towards_player
        #e.events[pygame.USEREVENT + 1] = q.move_right
        #e.events[pygame.USEREVENT + 2] = q.move_up
        #e.events[pygame.USEREVENT + 3] = q.move_down
        
        
        #Sets up exit button to quit game
        engine.events[pygame.QUIT] = engine.stop
        
        engine.run()
        
    def main():
        game = Game()

if __name__ == '__main__':
    Game().main()
