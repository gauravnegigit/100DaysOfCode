import random
import pymunk
import pygame 
import pymunk.pygame_util
from pymunk import Vec2d 

pygame.font.init()


# main screen constants 
WIDTH , HEIGHT = 700 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Tank")
FPS = 60 

# attributes of physical objects 
elasticity = 1

# font constants 
FONT = pygame.font.SysFont("comicsans" , 30)

def draw(space , draw_options , text):
	WIN.fill((0 , 0 , 0))
	WIN.blit(text , (10 , 10))
	space.debug_draw(draw_options)
	pygame.display.update()

def create_box(space , size , mass):
	body = pymunk.Body()
	body.position = Vec2d(random.randint(20 , 670) , random.randint(20 , 570))
	shape = pymunk.Poly.create_box(body , (size , size))
	shape.mass = mass 
	shape.friction = 0.7
	shape.elasticity = elasticity 
	space.add(body , shape)
	return body 


def create_segments(space ) :
    static = [
        [(0 , 0 ) , (WIDTH , 0 )] , 
        [(0 , 0 ) , (0 , HEIGHT)] , 
        [(WIDTH - 2, 0) , (WIDTH - 2, HEIGHT)] , 
        [(0 , HEIGHT - 2) , (WIDTH  , HEIGHT - 2)]
    ]

    for start , end in static : 
        shape = pymunk.Segment(space.static_body , start , end , 1.0)
        shape.elasticity = elasticity
        shape.friction = 0.5
        shape.color = (0 , 255 ,0 , 100)
        space.add(shape)

def pymunk_stuff():
	# pymunk main physics stuff 
	space = pymunk.Space()

	# creating segments around the edge of the screen 
	create_segments(space)

	# creating the boxes 
	for i in range(50):
		body = create_box(space , 20 , 1)
		pivot = pymunk.PivotJoint(space.static_body , body , (0 , 0) , (0 , 0))
		space.add(pivot)
		pivot.max_bias = 0
		pivot.max_force = 1000

		gear = pymunk.GearJoint(space.static_body , body , 0.0 , 1.0)
		space.add(gear)
		gear.max_bias = 0 
		gear.max_force = 5000 

	# creating the main tank in the simulation
	global tank_body , tank_box

	tank_body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
	tank_body.position = (WIDTH //2 , HEIGHT//2)
	space.add(tank_body)
	tank_box = create_box(space , 40 , 10)
	tank_box.position = (WIDTH //2 , HEIGHT//2)
	for s in tank_box.shapes :
		s.color = (0 , 255 , 100 , 100)

	# creating the pivot for the main tank
	pivot = pymunk.PivotJoint(tank_body , tank_box , ( 0 , 0) , (0 ,0 ))
	space.add(pivot)
	pivot.max_bias = 0 
	pivot.max_force = 10000

	gear = pymunk.GearJoint(tank_body , tank_box , 0.0 , 1.0)
	space.add(gear)
	gear.error_bias = 0 
	gear.max_bias = 1.2 
	pivot.max_force = 10000

	return space


def main():
	global tank_body , tank_box

	run = True 
	clock = pygame.time.Clock()

	space = pymunk_stuff()
	dt = 1/FPS
	draw_options = pymunk.pygame_util.DrawOptions(WIN)

	text = "USE THE MOUSE TO MOVE THE TANK ! "
	text = FONT.render(text , 1 , pygame.Color("white"))


	while run :
		clock.tick(FPS)
		space.step(dt)
		draw(space , draw_options , text)

		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_r :  
				run = False 

		pos = pygame.mouse.get_pos()
		d_mouse = pos - tank_box.position
		turn = tank_box.rotation_vector.cpvunrotate(d_mouse).angle
		tank_body.angle = tank_box.angle - turn 

		# driving the tank towardss the mouse 
		if tank_box.position.get_distance(pos) < 30 :
			tank_body.velocity = 0 , 0 
		else :
			if d_mouse.dot(tank_box.rotation_vector) > 0.0 :
				direction = 1.0 
			else :
				direction = -1.0 

			dv = Vec2d(100.0 * direction , 0.0)
			tank_body.velocity = tank_box.rotation_vector.cpvrotate(dv)


	main()

if __name__ == '__main__':
	main()