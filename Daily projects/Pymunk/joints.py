import random
import pygame
import pymunk 
import pymunk.pygame_util
pygame.font.init()

# main screen constants
WIDTH , HEIGHT = 800 , 600 
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Simulation using pymunk")
FPS = 60 

# attributes for real objects 
friction = 1
elasticity = 1.009

# font constants
FONT = pygame.font.SysFont("Arial Black" , 16)

def draw(space , draw_options):
    WIN.fill((255 , 255 , 255))
    space.debug_draw(draw_options)
    pygame.display.update()


def create_ball(space):
    mass = 1
    radius = 15 
    inertia = pymunk.moment_for_circle(mass , 0 , radius , (0 , 0))
    body = pymunk.Body(mass , inertia)
    x = random.randint(200 , 600)
    body.position = x , 10
    shape  = pymunk.Circle(body , radius )
    shape.friction = friction
    shape.elasticity = elasticity
    space.add(body , shape)
    return shape 


def create_static(space):
    """This function adds an inverted L shape between two joints"""


    limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    limit_body.position = (WIDTH//2 - 150  , HEIGHT//2)

    body = pymunk.Body(10, 10000)
    body.position = (WIDTH//2 , HEIGHT//2)
    l1 = pymunk.Segment(body, (-200, 0), (250.0, 0.0), 1)
    l2 = pymunk.Segment(body, (-200, 0), (-200.0, -50.0), 1)
    l1.friction = l2.friction = friction
    center_joint = pymunk.PinJoint(space.static_body , body, (WIDTH//2 , HEIGHT//2), (0, 0))
    joint_limit = 50
    limit_joint = pymunk.SlideJoint(
        body , limit_body , (-150 , 0), (0 , 0), 0, joint_limit
    )

    space.add(l1, l2, body, center_joint , limit_joint)
    return l1, l2


def main():
    run = True 
    clock = pygame.time.Clock()

    # pymunk basic variables
    space = pymunk.Space()
    space.gravity = (0 , 981 )
    

    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS

    balls = []

    ticks = 20  # this varibale is used for constantly creating teh balls under 1/3 seconds

    # creating the lines
    create_static(space)

    while run :
        clock.tick(FPS)
        space.step(dt)
        draw(space , draw_options)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_r :
                    run = False 
                    break
                    
                if event.key == pygame.K_p :
                    pygame.image.save()

        if ticks <= 0 :
            ticks = 20
            balls.append(create_ball(space))            

        ticks -= 1

        for ball in balls :
            if ball.body.position.y < 500 :
                balls.remove(ball)
    
    # the main method will be called recursively only under the condition that the user presses 'r'
    main()


if __name__ == "__main__":
    main()        