import math 
import random
import pymunk
import pygame 
import pymunk.pygame_util
from pymunk import Vec2d, moment_for_box 


# main screen constants
WIDTH , HEIGHT = 600 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60 

# attributes for pymunk objects
friction = 1.0
elasticity = 1.0


def draw(space , draw_options):
    WIN.fill((0 , 0 , 0 ))
    space.debug_draw(draw_options)


def create_logos(space , logos): 
    x = random.randint(15 , 400)
    y = 100
    angle = random.random() * math.pi 
    vertices = [(-20 , 20) , (20 , 20) , (0 , -20)]
    mass = 10 
    moment = pymunk.moment_for_poly(mass , vertices)
    body = pymunk.Body(mass , moment)
    shape = pymunk.Poly(body , vertices)
    shape.friction  = friction 
    shape.elasticity = elasticity
    body.position = x , y 
    body.angle = angle 

    space.add(body , shape)

    return shape

def main():
    run = True 
    clock = pygame.time.Clock()

    # PYMUNK STUFF 
    space = pymunk.Space()
    space.gravity = (0 , 981)
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS

    # logo
    logo_img = pygame.image.load("pymunk_logo.png")
    logos = []

    # creating the static lines 
    static_lines = [
        pymunk.Segment(space.static_body , (10.0 , 280.0) , (300.0 , 250.0) , 2.0) , 
        pymunk.Segment(space.static_body , (300.0 , 250.0) , (300.0 , 140.0) , 2.0) , 
    ] 

    for lines in static_lines :
        lines.friction = friction 
        lines.elasticity = elasticity

    space.add(*static_lines)

    ticks = 20 

    while run :
        clock.tick(FPS)
        space.step(dt)
        draw(space , draw_options)
        pygame.display.set_caption("fps : " + str(clock.get_fps()))


        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()

        ticks -= 1
        
        if ticks <= 0 :
            ticks = 20
            logos.append(create_logos(space , logos))
        
        for logo in logos :
            if logo.body.position.y < HEIGHT : 
                p = Vec2d(logo.body.position.x , logo.body.position.y) 
                
                #angle_degres = math.degrees(logo.body.angle) + 180 
                image = pygame.transform.rotate(logo_img , math.degrees(logo.body.angle))

                WIN.blit(image , (round(p.x - image.get_width() // 2) , round(p.y - image.get_height()//2)))

            else :
                logos.remove(logo)
                space.remove(logo.body , logo)
            
        pygame.display.update()

if __name__ == "__main__":
    main()