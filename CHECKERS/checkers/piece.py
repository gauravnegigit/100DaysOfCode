import pygame 
from .constants import RED, SQUARE_SIZE , WHITE , CROWN 


class Piece :
    PADDING = 20
    BORDER = 3
    def __init__(self , row , col , color) -> None:
        self.row = row 
        self.col = col 
        self.color = color 
        self.king = False # if the piece is a king then turn it to True 
        
        if self.color == RED :
            self.direction = -1 
        else :
            self.direction = 1
        
        
        self.x = 0 
        self.y = 0 
        self.calc_pos()
    
    def calc_pos(self ) :
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2
    

    def move(self , row , col) :
        self.row = row 
        self.col = col 
        self.calc_pos()

    def make_king(self) :
        self.king = True 
    
    def draw(self , win) : 
        radius = SQUARE_SIZE//2 - self.PADDING

        pygame.draw.circle(win , (128 , 128 , 128) , (self.x , self.y ) , radius + self.BORDER)
        pygame.draw.circle(win , self.color , (self.x   , self.y ) , radius)

        if self.king :
            win.blit(CROWN , (self.x - CROWN.get_width()//2 , self.y - CROWN.get_height()//2))


    def __repr__(self) -> str:
        return str(self.color)