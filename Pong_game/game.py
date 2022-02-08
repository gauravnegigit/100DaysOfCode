from client import WIDTH , HEIGHT
from Player import Player
from ball import Ball


#game variables

#paddles
paddle_height = 200
paddle_width = 50
color = (0,0,0)

#ball
ball_x , ball_y = WIDTH //2 - 10 , HEIGHT//2 - 10
dx , dy = 5,5
RADIUS = 20


class Game :
    def __init__(self , id ) -> None:
        self.ready = False
        self.id = id 
        self.ready = False
        self.players = [Player(100 , HEIGHT//2 - paddle_height//2 , paddle_width , paddle_height , color) , Player(850 , HEIGHT//2 - paddle_height//2 , paddle_width , paddle_height , color)]
        self.ball = Ball(ball_x , ball_y , RADIUS , (0 , 0 , 255))
    
    def connected(self):
        return self.ready 

    