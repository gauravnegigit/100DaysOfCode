import random
import math 
import pygame 
import pymunk
import pymunk.pygame_util

# main screen constants
WIDTH , HEIGHT = 600 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Planet simulation")
FPS = 60

# simualtion variables
gravityStrength = 5.0e6
elasticity = 0

def draw(space , draw_options):
    WIN.fill((0 , 0 , 0))

    # drawing the star at the centre of the screen 
    pygame.draw.circle(WIN, pygame.Color("yellow"), (300, 300), 10)

    space.debug_draw(draw_options)
    pygame.display.update()

def planetGravity(body , gravity , damping , dt):
    sq_dist = body.position.get_dist_sqrd((300 , 300))

    g = ((body.position - pymunk.Vec2d(300 , 300)) * -gravityStrength / (sq_dist * math.sqrt(sq_dist)))

    pymunk.Body.update_velocity(body , g , damping ,dt)

def add_circle(space):
    body = pymunk.Body()
    body.position = pymunk.Vec2d(random.randint(50 , 550) , random.randint(50 , 550))
    body.velocity_func = planetGravity 

    # calculating the distance from the centre
    r = body.position.get_distance((300 , 300))
    v = math.sqrt(gravityStrength / r)/ r 
    body.velocity = (body.position - pymunk.Vec2d(300 , 300)).perpendicular() * v 

    if body.position.get_distance((300 , 300)) > 50 :
        body.angular_velocity = v 
        body.angle = math.atan2(body.position.y , body.position.x)

        # creating the circle
        shape = pymunk.Circle(body , 10)
        shape.mass = 1
        shape.friction = 0.7
        shape.elasticity = elasticity 
        space.add(body , shape)

def main():
    global gravityStrength

    run = True 
    clock = pygame.time.Clock()

    # pymunk Physics stuff 
    space = pymunk.Space()
    space.gravity = (0 , 981)
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS

    # adding celestial objects 
    for i in range(30):
        add_circle(space)

    # main loop
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
                if event.key == pygame.K_p :
                    pygame.image.save(screen , "planet.png")

                if event.key == pygame.K_a :
                    for i in range(30):
                        add_circle(space)

                if event.key == pygame.K_SPACE :
                    gravityStrength += gravityStrength //10


if __name__ == '__main__':
    main()