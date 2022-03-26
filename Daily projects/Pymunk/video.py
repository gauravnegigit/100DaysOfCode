import time 
import random
import pygame 
import pymunk 
import pymunk.pygame_util
from pymunk import Vec2d 
import pymunk.autogeometry 


# main screen constants
WIDTH , HEIGHT = 800 , 350
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60 

#### image constants 
logo_img = pygame.image.load("pymunk_main_logo.png")

# attributes for pymunk objects
friction = 1.0
elasticity = 1.0

def draw(space , draw_options):
    WIN.fill((255 , 255 , 255))
    WIN.blit(logo_img , (0 , 0))
    space.debug_draw(draw_options)
    pygame.display.update()

# creating difefrent functions and assigning them different tasks to make different shapes 

def geometry(space):
    """This function is used for generating the geometry of the lgogo image"""
    logo_bb = pymunk.BB(0 , 0 , logo_img.get_width() , logo_img.get_height())

    def sample_func(point):
        try :
            p = pymunk.pygame_util.to_pygame(point , logo_img)
            color = logo_img.get_at(p)
            return color.a 
        
        except :
            return 0 

    logo_img.lock()
    lines = pymunk.autogeometry.march_soft(logo_bb , logo_img.get_width() , logo_img.get_height() , 99 , sample_func)
    logo_img.unlock()

    r = 10 
    letter_group = 0 

    for line in lines :
        line = pymunk.autogeometry.simplify_curves(line , 0.9)
        max_x = 0 
        max_y = 0 
        min_x = 1000
        min_y = 1000

        for l in line :
            max_x = max(max_x, l.x)
            min_x = min(min_x, l.x)
            max_y = max(max_y, l.y)
            min_y = min(min_y, l.y)

        w , h = max_x - min_x , max_y - min_y 

        if h < 30 :
            continue

        center = Vec2d(min_x + w /2.0 , min_y + h /2.0)
        t = pymunk.Transform(a = 1.0 , d = 1.0 , tx = - center .x , ty = -center.y )

        r += 30 
        if r < 255 :
            r = 0 

        for i in range(len(line) - 1):
            shape = pymunk.Segment(space.static_body, line[i], line[i + 1], 1)
            shape.friction = 0.5
            shape.color = (255, 255, 255, 255)
            space.add(shape)


def big_ball(space):
    mass = 1000
    radius = 50 
    moment = pymunk.moment_for_circle(mass , 0 , radius)
    body = pymunk.Body(mass , moment)
    shape  = pymunk.Circle(body , radius)
    shape.friction = friction 
    shape.elasticity = elasticity
    shape.color = (255 , 0 , 0 , 100)
    body.position = (900 , 100)
    body.apply_impulse_at_local_point((-10000 , 0) , (0 , 0))
    space.add(body , shape)

def boxfloor(space):
    mass = 10 
    vertices = [(-50 , 30) , (60 , 22) , (-50 , 22)]
    moment = pymunk.moment_for_poly(mass , vertices)
    body = pymunk.Body(mass , moment)
    s = pymunk.Poly(body , vertices)
    s.color = (0 , 0 , 0 , 255)
    body.position = (600 , 75)

    space.add(body , s)

def create_box(space):
    """this function is used to create the box in the simulation """

    mass = 10 
    moment = pymunk.moment_for_box(mass , (40 , 20))
    b = pymunk.Body(mass , moment)
    shape = pymunk.Poly.create_box(b , (40 , 20))
    shape.friction = friction 
    b.position = 600 ,  50 
    space.add(b , shape)

def car(space):
    """This function is used for creating a car"""

    pos = Vec2d(100 , 200)
    
    wheel_color = 52, 219, 119, 255
    shovel_color = 219, 119, 52, 255
    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass , 20 , radius)
    w1 = pymunk.Body(mass , moment)
    w2 = pymunk.Body(mass , moment)
    s_w1 = pymunk.Circle(w1 , radius)
    s_w2 = pymunk.Circle(w2 , radius)

    s_w1.color = s_w2.color = wheel_color
    s_w1.elasticity = s_w2.elasticity = elasticity
    s_w1.friction =  s_w2.friction = friction 

    space.add(w1 , s_w1)
    space.add(w2 , s_w2)

    size = (50 , 30)
    moment = pymunk.moment_for_box(mass , size)
    chassi = pymunk.Body(mass , moment)
    s_chassi = pymunk.Poly.create_box(chassi , size)

    space.add(chassi , s_chassi)

    vs = [(0 , 0 ) , (25 , 45) , (0 , 45)]
    shovel = pymunk.Poly(chassi , vs , transform = pymunk.Transform(tx = 85))
    shovel.friction = friction 
    shovel.elasticity = elasticity
    shovel.color = shovel_color

    space.add(shovel)

    w1.position = pos - (60 , 0)
    w2.position = pos + (60 , 0)
    chassi.position = pos + (0 , -25)

    space.add(
        pymunk.PinJoint(w1 , chassi , (0 , 0) , (-25 , -15)) , 
        pymunk.PinJoint(w1 , chassi , (0 , 0) , (-25 , 15)) , 
        pymunk.PinJoint(w2 , chassi , (0 , 0) , (25 , -15)) , 
        pymunk.PinJoint(w2 , chassi , (0 , 0) , (25 , 15))
    )

    speed = 20
    space.add(
        pymunk.SimpleMotor(w1 , chassi , speed) , 
        pymunk.SimpleMotor(w2 , chassi , speed) , 
    )

def cannon(space):
    mass = 100
    radius = 20
    moment = pymunk.moment_for_circle(mass , 0 , radius)
    b = pymunk.Body(mass , moment)
    b.position = 700 , -50
    s = pymunk.Circle(b , radius)
    s.color = (255 , 0 , 0 , 100)
    b.apply_impulse_at_local_point((-250000 , 75000))
    space.add(b , s)

def main():
    run = True 
    clock = pygame.time.Clock()

    # PYMUNK STUFF 
    space = pymunk.Space()
    space.gravity = (0 , 981)
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS

    # adding normal floor to the space 
    floor = pymunk.Segment(space.static_body, (-100, 300), (1000, 220), 5)
    floor.friction = 1.0
    space.add(floor)

    time1 = time.time()

    # creating a list of all the events 

    events = []
    events.append((0.1, big_ball))
    events.append((2, big_ball))
    events.append((3.5, boxfloor))
    for x in range(8):
        events.append((4 + x * 0.2, create_box))
    events.append((6.5, car))
    events.append((8.5, cannon))

    total_time = 0        # this variable will keep track of time 

    time1 = time.time()
    time2 = None 

    # generating the geeometry of the image 
    geometry(space)

    while run :
        ft = clock.tick(FPS)
        space.step(dt)
        draw(space , draw_options)

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()

        if time2 and time2 - time1 <= 0.5 :
            """If 0.4 second have passed then 100 small balls will be generated """
            """In this code the amount of balls generated may also depend on the speed of the computer ."""

            for i in range(10):
                mass = 1
                radius = 8 
                moment = pymunk.moment_for_circle(mass , 0 , radius)
                b =pymunk.Body(mass , moment)
                shape = pymunk.Circle(b , radius)
                shape.frcition = friction 
                shape.elasticity = 0.5
                x = random.randint(100 , 400)
                b.position = x, -10
                space.add(b , shape)

        if len(events) > 0 and total_time > events[0][0]:
            t, f = events.pop(0)

            f(space)       
        
        total_time += ft / 1000.0
        time2 = time.time()

if __name__ == "__main__":
    main()