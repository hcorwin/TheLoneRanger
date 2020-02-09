#!/usr/bin/env python3
import pygame
import sys
sys.path.append('../')
import league
from player import Player
from zombie import Zombie
from overlay import Overlay
from random import *



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

    def spawn_zombies(t):
        r1 = randint(1, 800)
        r2 = randint(1, 600)
        z = Zombie(t.player, 0, t.player.x + 100, t.player.y + 100)
        t.engine.objects.append(z)
        t.engine.drawables.add(z)
        # Register collisions for zombies
        t.engine.collisions[t.player] = (z, t.player.ouch)
        # Register zombie movements in event list
        t.engine.events[pygame.USEREVENT] = t.zombies.move_towards_player

    # Create engine
    engine = league.Engine("The Lone Ranger")
    engine.init_pygame()

    # Setup the world
    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    backgroundTiles = league.Tilemap('./assets/background.lvl', sprites, layer=0)
    foregroundTiles = league.Tilemap('./assets/world.lvl', sprites, layer=1)
    world_size = (
    foregroundTiles.wide * league.Settings.tile_size, foregroundTiles.high * league.Settings.tile_size)
    engine.drawables.add(backgroundTiles.passable.sprites())
    engine.drawables.add(foregroundTiles.passable.sprites())

    # Create player object
    player = Player(2, 400, 300)
    player.blocks.add(foregroundTiles.impassable)
    player.world_size = world_size
    player.rect = player.image.get_rect()
    engine.objects.append(player)
    engine.drawables.add(player)

    # Create overlay
    overlay = Overlay(player)
    engine.objects.append(overlay)
    engine.drawables.add(overlay)

    # Create initial zombies
    numZombies = 4
    zombies = []
    randNum = 0

    for zombie in range(0, numZombies):
        zombies.append(Zombie(player, 10, 100 + randNum, 500 + randNum))
        engine.objects.append(zombies[zombie])
        engine.drawables.add(zombies[zombie])
        randNum = randint(1, 400)
        # Register collisions for zombies
        engine.collisions[player] = (zombies[zombie], player.ouch)
        # Register events
        pygame.time.set_timer(pygame.USEREVENT + zombie, 500 // league.Settings.gameTimeFactor)
        # Register zombie movements in event list
        engine.events[pygame.USEREVENT + zombie] = zombies[zombie].move_towards_player

    spawn_zombie = pygame.USEREVENT + 4
    pygame.time.set_timer(spawn_zombie, 1000)
    engine.events[spawn_zombie] = spawn_zombies

    # Create camera that follows player
    camera = league.LessDumbCamera(800, 600, player, engine.drawables, world_size)
    engine.objects.append(camera)
    engine.objects.append(camera)

    # Player movements
    engine.key_events[pygame.K_a] = player.move_left
    engine.key_events[pygame.K_d] = player.move_right
    engine.key_events[pygame.K_w] = player.move_up
    engine.key_events[pygame.K_s] = player.move_down

    # Sets up exit button to quit game
    engine.events[pygame.QUIT] = engine.stop

    engine.run()


def main(self):
    game = Game()

if __name__ == '__main__':
    Game().main()
