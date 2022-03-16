import pygame 
import pymunk 
import pymunk.pygame_util
from pymunk import Vec2d 


# main screen variable constants 
WIDTH , HEIGHT = 800 , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60
pygame.display.set_caption("Pyramid")

# variables 
drawing = True #The user can turn it false by pressing the space key 

def draw(space , draw_options):
	WIN.fill((0 , 255 , 0))
	space.debug_draw(draw_options)
	pygame.display.update()


def pyramid(space ):
	x = Vec2d(-270 , 7.5) + (400 , 200)
	y = Vec2d(0 , 0)
	deltaX = Vec2d(0.5625, 1.1) * 20
	deltaY = Vec2d(1.125, 0.0) * 20

	for i in range(25):
		y = Vec2d(*x)
		for j in range(i , 25):
			size = 10 
			points = [(-size , -size) , (-size , size) , (size , size) , (size , -size)]
			mass = 1.0
			moment = pymunk.moment_for_poly(mass , points , (0 , 0))
			body = pymunk.Body(mass , moment)
			body.position = y 
			shape = pymunk.Poly(body , points)
			shape.friction = 1
			shape.elasticity = 1.07

			space.add(body , shape)

			y += deltaY

		x += deltaX

	pymunk.pygame_util.positive_y_is_up = True

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
        shape.elasticity = 1.07
        shape.friction = 1
        shape.color = (0 , 0 , 255, 100)
        space.add(body , shape)

def main():
	global drawing

	run = True
	clock = pygame.time.Clock()

	# main pymunk varaibles 

	space = pymunk.Space()
	space.gravity = (0 , -980)
	draw_options = pymunk.pygame_util.DrawOptions(WIN)
	dt = 1/FPS

	# creating a segment as a ground
	shape = pymunk.Segment(space.static_body , (5 , 100) , (595 , 100) , 1.0)

	create_boundaries(space , WIDTH , HEIGHT)


	# draw options for drawing the pyramid 
	pyramid(space)

	while run :
		clock.tick(FPS)
		space.step(dt)

		if drawing :
			draw(space , draw_options)

		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False
				pygame.quit()
				quit()

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
				drawing = not drawing
				


if __name__ == '__main__':
	main()