
import pygame
from network import Network 

pygame.font.init()


# screen variables
WIDTH = 1000 
HEIGHT = 600 

# score variabless
left_score  , right_score = 0 ,0

# to avoid running the window as client.py is also imported on server.py and player.py 
if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH , HEIGHT))
    pygame.display.set_caption("Pong game using Python")

FPS = 60 

#game variables
RADIUS = 20

# color variables
GREEN = (0 , 255 , 0) 
BLACK = (0,0,0)
BLUE = (0, 0 ,255)

#font variables
SCORE = pygame.font.SysFont("ARIAL BALCK" , 40)
font = pygame.font.SysFont("ARIAL BLACK" , 40)

def redraw(game , player1 , player2 , ball1 , ball2 ):


    WIN.fill((128 , 128 , 128))

    if not (game.connected()) :
        font = pygame.font.SysFont("ARIAL BLACK"  , 40)
        text = font.render('WAITING FOR PLAYER ....' , 1 , (255 , 0 , 0 ))
        WIN.blit(text , (WIDTH //2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))

    else :
        WIN.fill(GREEN)
        player1.draw(WIN)
        player2.draw(WIN)
        text = SCORE.render("LEFT PLAYER : "+str(left_score)+ "  RIGHT PLAYER : "+str(right_score),1,BLUE)
        WIN.blit(text,(WIDTH//2 - text.get_width()//2,10))
        
        ball1.draw(WIN)
        ball2.draw(WIN)


    pygame.display.update()

def main():
    global left_score , right_score

    run = True
    n = Network()
    p1 = n.getP()

    ball1 = n.getB()
    
    clock = pygame.time.Clock()

    #initializing ball variables
    ball_x , ball_y = WIDTH //2 - 10 , HEIGHT//2 - 10
    dx , dy = 5,5


    while run :
        clock.tick(FPS)

        try :
            game = n.send("get")
        except :
            run = False
            print("Couldn't get the game !")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
    

        # conditions for the ball
        if ball1.y<30 or ball1.y > HEIGHT - 30:
            dy *= -1
        if ball1.x < 2 * RADIUS :
            right_score += 10
            ball1.x,ball1.y = WIDTH//2 , HEIGHT//2
        if ball1.x > WIDTH - 2 * RADIUS :
            left_score += 10
            ball1.x,ball1.y = WIDTH//2 , HEIGHT//2

        p2 , ball2 =  n.send((p1 , ball1))


        # if the ball strikes the left and the right paddle
        
        # since both the players would think they are the 1st player
        if p1.x < WIDTH//2 :
            if 0 < ball1.x - p1.x < p1.width + RADIUS and -RADIUS < ball1.y - p1.y < p1.height + RADIUS:
                dx *= -1      

        elif p1.x > WIDTH //2 :   
            if 0 < p1.x - ball1.x < p1.width - RADIUS and -RADIUS < ball1.y-p1.y< p1.height + RADIUS:
                dx *= -1     
        
        # since both the players would think their opponent is the second player
        if p2.x < WIDTH//2 :
            if 0 < ball1.x - p2.x < p2.width + RADIUS and -RADIUS < ball1.y - p2.y < p2.height + RADIUS:
                dx *= -1  
        
        elif p2.x > WIDTH//2 :
            if 0 < p2.x - ball1.x < p2.width - RADIUS and -RADIUS < ball1.y-p2.y< p2.height + RADIUS:
                dx *= -1            

        # moving the player and the ball
        if game.connected() :
            ball1.move(dx , dy)

        p1.move()
        redraw(game , p1 , p2 , ball1 , ball2 ) 


def main_menu():
    run = True 
    clock = pygame.time.Clock()
    while run :
        clock.tick(FPS)
        WIN.fill((128 , 128 , 128))
        text = font.render("Click to Play!", 1, (255,0,0))
        WIN.blit(text, (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                run = False
                break
    main()

if __name__ == "__main__":
    main_menu()