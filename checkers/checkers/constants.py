import pygame

WIDTH, HEIGHT =800, 800
ROWS, COLS= 10, 10
SQUARE_SIZE=WIDTH//COLS

#rgb
RED=(200, 0, 0)
WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREY=(128,128,18)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45,25))