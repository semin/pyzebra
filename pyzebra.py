#!/usr/bin/env python

##    pyzebra
##    Copyright (C) 2008-2011 Semin Lee
##
##    Semin Lee
##    seminlee at gmail dot com
##


"""
pyzebra was created by Semin Lee for Dr. Joonyoung Kim's experiments.
"""

import pygame
from pygame import surfarray
from pygame.locals import *
from sys import exit

pygame.init()
pygame.key.set_repeat()

screen_width, screen_height = pygame.display.list_modes()[0]
screen  = pygame.display.set_mode((screen_width, screen_height), HWSURFACE | FULLSCREEN, 8)
font    = pygame.font.SysFont("arial", 16)
clock   = pygame.time.Clock()

column_surface  = pygame.image.load("column.jpg").convert()
column_color    = (255, 255, 255)
column_width    = 100.
column_gap      = 100.
column_speed    = 100.
column_pos_x    = 0.
direction       = "right"
temp_speed      = 0.

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    pygame.event.pump()
    pressed_keys = pygame.key.get_pressed()
        
    if pressed_keys[K_RIGHT]:
        direction = "right"
    if pressed_keys[K_LEFT]:
        direction = "left"
    if pressed_keys[K_LSHIFT] and pressed_keys[K_s]:
        column_speed += 1
    if not pressed_keys[K_LSHIFT] and pressed_keys[K_s]:
        column_speed -= 1
    if pressed_keys[K_LSHIFT] and pressed_keys[K_g]:
        column_gap += 1
    if not pressed_keys[K_LSHIFT] and pressed_keys[K_g]:
        column_gap -= 1
    if pressed_keys[K_LSHIFT] and pressed_keys[K_w]:
        column_width += 1
    if not pressed_keys[K_LSHIFT] and pressed_keys[K_w]:
        column_width -= 1
    if pressed_keys[K_ESCAPE]:
        exit()
    if pressed_keys[K_SPACE]:
        if int(column_speed) == 0:
            column_speed = temp_speed
        else:
            temp_speed = column_speed
            column_speed = 0.
    
    column_interval = column_width + column_gap
    scaled_column_surface = pygame.transform.scale(column_surface, (column_width, screen_height))

    screen.fill((0, 0, 0))
    
    text = "* pyzebra configuration: \
    Direction [<-/->]: %(direction)s, \
    Column width [W/w]: %(width)dx, \
    Gap width [G/g]: %(gap)dpx, \
    Speed [S/s]: %(speed)dpx per second, \
    Start/Stop [space], \
    Quit [esc]" \
    % {'direction': direction, 'width':column_width, 'gap':column_gap, 'speed':column_speed }
            
    banner = font.render(text, True, (85,107,47), (0, 0, 0))
    screen.blit(banner, (0,0))
    
    for x in range(0, screen_width * 2, int(column_interval)):
        screen.blit(scaled_column_surface, (column_pos_x + x, 20))
        screen.blit(scaled_column_surface, (column_pos_x - x, 20))
        # pygame.draw.rect(screen, column_color, Rect(column_pos_x + x, 20, column_width, screen_height))
        # pygame.draw.rect(screen, column_color, Rect(column_pos_x - x, 20, column_width, screen_height))

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0

    distnace_moved = time_passed_seconds * column_speed

    if direction == "right":
        column_pos_x += distnace_moved
    
        if column_pos_x > screen_width:
            column_pos_x -= (int(screen_width / column_interval) + 1) * column_interval
    else:
        column_pos_x -= distnace_moved
    
        if column_pos_x < 0:
            column_pos_x += (int(screen_width / column_interval) + 1) * column_interval
    
    pygame.display.update()
