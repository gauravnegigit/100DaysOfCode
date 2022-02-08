
import pygame


class Player :
    def __init__(self , x  , y ,width , height , color) -> None:
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.color = color
        self.vel = 10
    
    def draw(self , win):
        pygame.draw.rect(win , self.color , (self.x , self.y ,self.width , self.height))
    
    def move(self):
        keys = pygame.key.get_pressed()


        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y < 600 - self.height:
            self.y += self.vel  
 

