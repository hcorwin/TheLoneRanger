#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from zombie import Zombie
from overlay import Overlay

"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

# Function to call when colliding with zombie

def main():
    
    e = league.Engine("The Lone Ranger")
    e.init_pygame()

    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    t = league.Tilemap('./assets/world.lvl', sprites, layer = 1)
    b = league.Tilemap('./assets/background.lvl', sprites, layer = 0)
    world_size = (t.wide * league.Settings.tile_size, t.high * league.Settings.tile_size)
    
    e.drawables.add(t.passable.sprites())
    e.drawables.add(b.passable.sprites())
    
    p = Player(2, 400, 300)
    o = Overlay(p)
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()
    
    q = Zombie(p, 10, 100, 500)
    q1 = Zombie(p, 10, 600, 700)
    q2 = Zombie(p, 10, 300, 400)
    q3 = Zombie(p, 10, 500, 200)

    e.objects.append(p)
    e.objects.append(q)
    e.objects.append(q1)
    e.objects.append(q2)
    e.objects.append(q3)
    
    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(q1)
    e.drawables.add(q2)
    e.drawables.add(q3)
    
    e.drawables.add(o)
    
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    
    e.objects.append(c)
    e.objects.append(o)

    e.collisions[p] = (q, p.ouch)
    #need to register more collisions with new zombie here
    
    #Register events?
    pygame.time.set_timer(pygame.USEREVENT + 0, 1000 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 4, 1000 // league.Settings.gameTimeFactor)
    #Player movements

    e.key_events[pygame.K_a] = p.move
    e.key_events[pygame.K_d] = p.move
    e.key_events[pygame.K_w] = p.move
    e.key_events[pygame.K_s] = p.move
    

    def prin(t):

        z = Zombie(p,10, p.x + 10, p.y +10)
        e.drawables.add(z)
        e.objects.append(z)

    def updateZoms(time):
        for i in e.objects:
            if isinstance(i,Zombie):
                i.move_towards_player(time)
            
                
    

    #Register zombie movements in event list
    e.events[pygame.USEREVENT + 0] = q.move_towards_player
    e.events[pygame.USEREVENT + 1] = q1.move_towards_player
    e.events[pygame.USEREVENT + 2] = q2.move_towards_player
    e.events[pygame.USEREVENT + 3] = updateZoms
    e.events[pygame.USEREVENT + 4] =  prin
    #e.events[pygame.USEREVENT + 1] = q.move_right
    #e.events[pygame.USEREVENT + 2] = q.move_up
    #e.events[pygame.USEREVENT + 3] = q.move_down
    
    
    #Sets up exit button to quit game
    e.events[pygame.QUIT] = e.stop
    
    
    #Runs the main game loop
    e.run()

    

if __name__=='__main__':
    main()
