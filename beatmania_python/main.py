import pygame
import sys
import os

screen_width, screen_height = 800, 600

fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

pos_a = 187
pos_b = 258
pos_c = 329
pos_d = 400
pos_e = 471
pos_f = 542

speed = 3
visual_latency = 80

strum_position = 500

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
strum = pygame.image.load('assets/notestrum.png')
pressed = pygame.image.load('assets/pressed.png')
pygame.display.set_caption('Beatmania Python')

