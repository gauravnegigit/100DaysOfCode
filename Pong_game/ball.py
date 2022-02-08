import pygame

class Ball :
    def __init__(self , x  , y ,radius , color) -> None:
        self.x = x 
        self.y = y 
        self.radius = radius 
        self.color = color
        self.vel = 10

    
    def draw(self , win):
        pygame.draw.circle(win , self.color , (self.x , self.y ) , self.radius)
    
    def move(self , dx , dy):
        self.x += dx 
        self.y += dy