from pickle import TRUE
import random 
import pygame 
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d 


# main screen constants
WIDTH , HEIGHT = 600 , 600
WIN  = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60 
pygame.display.set_caption("Camera simulation using pymunk")

drawing = True            # may be turned into False in order to pause the simulation 

# attributes for objects 
friction = elasticity = 1 

def draw(space , draw_options , scaling , rotation , translation):
    WIN.fill((255 , 255 , 255))
    space.debug_draw(draw_options)

    draw_options.transform = (
        pymunk.Transform.translation(WIDTH //2 , HEIGHT //2)
        @ pymunk.Transform.scaling(scaling)
        @ translation
        @ pymunk.Transform.rotation(rotation)
        @ pymunk.Transform.translation(-WIDTH //2 , - HEIGHT //2)
    )

    pygame.display.update()


def background_stuff(space ):
    balls = []

    body = pymunk.Body()
    body.position = pymunk.Vec2d(407, 354)
    s1 = pymunk.Segment(body, Vec2d(-300, -30), Vec2d(0, 0), 1.0)
    s2 = pymunk.Segment(body, Vec2d(0, 0), Vec2d(0, -100), 1.0)
    s1.density = 0.1
    s2.density = 0.1
    s1.friction = s2.friction = friction
    s1.elasticity = s1.elasticity = elasticity
    space.add(body, s1, s2)

    c1 = pymunk.constraints.DampedSpring(
        space.static_body,
        body,
        (427, 200),
        (0, -100),
        Vec2d(407, 254).get_distance((427, 200)),
        2000,
        100,
    )

    c2 = pymunk.constraints.DampedSpring(
        space.static_body,
        body,
        (87, 200),
        (-300, -30),
        Vec2d(107, 324).get_distance((87, 200)),
        2000,
        100,
    )
    space.add(c1, c2)

    # extra to show how constraints are drawn when very small / large
    body = pymunk.Body(1, 100)
    body.position = 450, 305
    c3 = pymunk.constraints.DampedSpring(
        space.static_body, body, (450, 300), (0, 0), 5, 1000, 100
    )
    space.add(body, c3)
    body = pymunk.Body(1, 100)
    body.position = 500, 2025
    c3 = pymunk.constraints.DampedSpring(
        space.static_body, body, (500, 25), (0, 0), 2000, 1000, 100
    )
    space.add(body , c3)


def main():
    global drawing 

    run = True 
    clock = pygame.time.Clock()

    # pymunk variables
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS 
    translation = pymunk.Transform()
    rotation , scaling = 0 , 1

    zoom_in = zoom_out = 0          # variables for zooming the simulation 

    background_stuff(space)
    ticks = 20 

    # game variables 
    shapes = []

    while run :
        clock.tick(FPS)
        space.step(dt)

        if drawing : 
            draw(space , draw_options , scaling , rotation , translation)
            space.gravity = (0 , 981)
            ticks -= 1
        
        else :
            space.gravity = (0 , 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN :

                if event.key == pygame.K_p :
                    pygame.image.save()
                
                elif event.key == pygame.K_r :
                    run = False 
                    break 
            
                elif event.key == pygame.K_SPACE :
                    drawing  = not drawing 

        keys = pygame.key.get_pressed()   # here keys is a dictionary containing different values of pressed keys 

        # when a key get pressed the condition will be true and so in integer form it would be 1 

        left = int(keys[pygame.K_LEFT])
        right = int(keys[pygame.K_RIGHT])
        up = int(keys[pygame.K_UP])
        down = int(keys[pygame.K_DOWN])


        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] :
            zoom_in = int(keys[pygame.K_EQUALS])
            zoom_out = int(keys[pygame.K_MINUS])

        zoom_speed = 0.1 
        scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

        rotate_left = int(keys[pygame.K_LSHIFT])
        rotate_right = int(keys[pygame.K_RSHIFT])

        translation = translation.translated(10 * left - 10 * right , 10 * up - 10 * down)

        rotation_speed = 0.05
        rotation += (rotate_left - rotate_right ) * rotation_speed

        if ticks <= 0 :
            ticks = 20 
            mass = 10 
            radius = 25 
            moment = pymunk.moment_for_circle(mass , 0 , radius ,(0 ,0))
            body = pymunk.Body(mass , moment)
            x = random.randint(120 , 350)

            body.position = x , 100 

            if random.randint(1 , 2) == 1 :
                shape = pymunk.Circle(body , radius)
            
            else :
                shape = pymunk.Poly.create_box(body , (radius * 2 , radius * 2) , 2)

            shape.friction = friction
            shape.elasticity = elasticity
            space.add(body , shape)
            shapes.append(shape)

        for shape in shapes :
            if shape.body.position.y > 550 :
                space.remove(shape , shape.body)
                shapes.remove(shape)
    
    main()               # this function will run recursively if the user pressed the r button 

            
if __name__ == "__main__":
    main()