import random
import pygame 
import pymunk 
import pymunk.pygame_util

# main screen constants 
WIDTH , HEIGHT = 600 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Newton's cradle ")
FPS = 60 

# simulation variables 
elasticity = 1 

def draw(space , draw_options):
    WIN.fill((0 , 0 , 0))
    space.debug_draw(draw_options)
    pygame.display.update()

def reset_bodies(space):
    for body in space.bodies:
        body.position = pymunk.Vec2d(*body.start_position)
        body.force = 0, 0
        body.torque = 0
        body.velocity = 0, 0
        body.angular_velocity = 0
    color = pygame.Color(
        random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)
    )
    for shape in space.shapes:
        shape.color = color



def main():
    run = True 
    clock = pygame.time.Clock()

    # pymunk physics stuff
    space = pymunk.Space()
    space.gravity = (0 , 981)
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS


    # creating cradles 
    bodies = []
    for x in range(-100 , 150 , 50):
        x += WIDTH / 2
        offset_y = HEIGHT//2

        mass = 10 
        radius = 25 
        moment = pymunk.moment_for_circle(mass , 0 , radius , (0 , 0))
        body = pymunk.Body(mass , moment)

        body.position = (x , 150 + offset_y)
        body.start_position = pymunk.Vec2d(*body.position)
        shape = pymunk.Circle(body , radius)
        shape.elasticity = elasticity
        bodies.append(body)
        j = pymunk.PinJoint(space.static_body, body , (x , -150 + offset_y) , (0 ,0))
        space.add(body , shape , j)

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
                if event.key == pygame.K_SPACE :
                    r = random.randint(1, 4)
                    for body in bodies[0:r]:
                        body.apply_impulse_at_local_point((-6000, 0))

                if event.key == pygame.K_r :
                    reset_bodies(space )


if __name__ == '__main__':
    main()