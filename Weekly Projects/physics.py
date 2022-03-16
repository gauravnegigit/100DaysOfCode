import pygame 
import math 
import pymunk
import pymunk.pygame_util
pygame.init()


# main screen constants 
WIDTH , HEIGHT = 1000 , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 120

def calculate_distance(p1 , p2):
    """This function helps us to calculate the distancebetween two points"""

    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)

def calculate_angle(p1 , p2):
    """
    This function helps us to calculate the angle between two points 
    """
    return math.atan2(p2[1] - p1[1] , p2[0] - p1[0])

def draw(space , window , draw_options , line) :
    WIN.fill((255 , 255 , 255))
    if line :
        pygame.draw.line(window , "black" , line[0] , line[1])

    space.debug_draw(draw_options)
    pygame.display.update()

    
def create_ball(space , radius , mass , pos) :
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos 
    shape = pymunk.Circle(body , radius)
    shape.mass = mass 
    shape.color = (255 , 0 , 0 , 100)
    shape.elasticity = 1
    shape.friction = 0.4
    space.add(body , shape)
    return shape 

def create_pendulum(space) :
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300 , 270)

    body = pymunk.Body()
    body.position = (300 , 300)
    line = pymunk.Segment(body , (0,0), (255 , 0) , 5)
    circle = pymunk.Circle(body , 40 , (255 , 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.9
    rotation_center_joint = pymunk.PinJoint(body , rotation_center_body , (0 , 0))

    space.add(circle , line , body , rotation_center_joint)


def create_boundaries(space , width , height) :
    rects = [
        [(width/2 , height - 15) , (width , 30)] , 
        [(width/2 , 15) , (width , 30)] ,
        [(15 , height/2) , (30 , height) ] , 
        [(width - 15 , height/2) , (30 , height)]
    ]

    for pos , size in rects :
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos 
        shape = pymunk.Poly.create_box(body , size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        shape.color = (255 , 128 , 128 , 100)
        space.add(body , shape)

def create_structure(space  ,height) :
    """This function does the job of creating a structure
    """

    BROWN = (139 , 69 , 19 , 100)
    rects = [
        [(600 , height - 120) , (40 , 200)  ] , 
        [(900 , height - 120) , (40 , 200)] ,
        [(750 , height - 240) , (340 , 40) ] , 
        [(750 , height - 20) , (260 , 40) ]
    ] 

    for pos , size in rects :
        body = pymunk.Body()
        body.position = pos 
        shape = pymunk.Poly.create_box(body , size , radius = 2)
        shape.mass = 10
        shape.elasticity = 0.4
        shape.friction = 0.4
        shape.color = BROWN 
        space.add(body , shape)

def main() :
    run = True 

    # pymunk main basic variables
    space = pymunk.Space()
    space.gravity = (0 , 981)
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS

    # main game variables
    ball = None 
    line = None 
    pressed_pos = None 

    create_boundaries(space , WIDTH , HEIGHT)
    create_structure(space , HEIGHT)
    create_pendulum(space)


    clock = pygame.time.Clock()
    while run :
        clock.tick(FPS)
        space.step(dt)

        if ball and pressed_pos :
            line = [pressed_pos , pygame.mouse.get_pos()]

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN :
                if not ball :
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space , 30 , 10 , pressed_pos)
                
                elif pressed_pos :
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 100
                    fx , fy = math.cos(angle) * force , math.sin(angle) * force

                    ball.body.apply_impulse_at_local_point((fx , fy ) , (0,0))
                    pressed_pos = None 
                else :
                    space.remove(ball , ball.body)
                    ball = None 

        draw(space , WIN , draw_options , line)


if __name__ == "__main__" :
    main()