import pygame

# main screen constants 
WIDTH , HEIGHT = 800 , 800
ROWS , COLUMNS = 8 , 8 
SQUARE_SIZE = WIDTH//COLUMNS

# color constants
RED = (255 , 0 , 0)
WHITE = (255 , 255 , 255)
BLUE = (0 , 0 , 255)
BLACK = (0,0,0)

CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png") , (40 , 25))

