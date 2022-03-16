import pygame 
import random
import pymunk 
import pymunk.pygame_util
from pymunk import Vec2d 


# main screen constants 
WIDTH , HEIGHT = 600 , 600 
WIN  = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60

# game variables
elasticity = 1

def draw(space , draw_options):
	WIN.fill(pygame.Color("lightgrey"))
	space.debug_draw(draw_options)
	pygame.display.update()


def create_flippers(space):
	# variable for the flippers
	fp = [(20, -20), (-120, 0), (20, 20)]
	mass = 100
	moment = pymunk.moment_for_poly(mass, fp)

	# left flipper 
	l_body = pymunk.Body(mass , moment)
	l_body.position = 150 , 500
	l_shape = pymunk.Poly(l_body , [(-x , y) for x , y in fp])
	l_shape.elasticity = elasticity
	space.add(l_body , l_shape)

	l_joint = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
	l_joint.position = l_body.position
	j = pymunk.PinJoint(l_body , l_joint, (0 , 0 ) , (0 , 0))
	s = pymunk.DampedRotarySpring(l_body , l_joint , -0.15 , 20000000, 900000)

	space.add(j , s)

	# right flipper 
	r_body = pymunk.Body(mass , moment)
	r_body.position = 450 , 500
	r_shape = pymunk.Poly(r_body , fp)
	r_shape.elasticity = elasticity
	space.add(r_body , r_shape)

	r_joint = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
	r_joint.position = r_body.position
	j = pymunk.PinJoint(r_body , r_joint , (0 , 0 ) , (0 , 0))
	s = pymunk.DampedRotarySpring(r_body , r_joint , 0.15 , 20000000 , 900000)

	space.add(j , s)

	return l_shape , r_shape

def create_boundaries(space , width , height):
	static_lines = [
	    pymunk.Segment(space.static_body, (150, 500), (50, 50), 1.0),
	    pymunk.Segment(space.static_body, (450, 500), (550, 50), 1.0),
	    pymunk.Segment(space.static_body, (50, 50), (300, 0), 1.0),
	    pymunk.Segment(space.static_body, (300, 0), (550, 50), 1.0),
	    pymunk.Segment(space.static_body, (300, 180), (400, 200), 1.0),
	    pymunk.Segment(space.static_body, (210 , 200), (300, 180), 1.0)
	]

	for line in static_lines :
		line.elasticity = elasticity
		line.friction = 0.1

	space.add(*static_lines)

	rects = [ 
		[(5 , height/2) , (10 , height) ] , 
		[(width - 5 , height/2) , (10 , height)]
	]

	for pos , size in rects :
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = pos 
		shape = pymunk.Poly.create_box(body , size)
		shape.elasticity = 1.07
		shape.friction = 1
		shape.color = (0 , 0 , 255, 100)
		space.add(body , shape)

def create_bumpers(space):
	for p in [(240, 100), (360, 100)]:
	    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
	    body.position = p
	    shape = pymunk.Circle(body, 10)
	    shape.elasticity = elasticity
	    space.add(body, shape)	


def main():
	run = True 
	clock = pygame.time.Clock()

	# pymunk basic variables
	space = pymunk.Space()
	space.gravity = (0 , 900)
	draw_options = pymunk.pygame_util.DrawOptions(WIN)
	dt = 1/FPS

	# game variables
	balls = []

	l , r = create_flippers(space)
	create_boundaries(space , WIDTH , HEIGHT)
	create_bumpers(space)

	while run :
		clock.tick(FPS)
		space.step(dt)
		draw(space , draw_options)

		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				run = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_f :
					l.body.apply_impulse_at_local_point(Vec2d.unit() * 40000 , (- 100 , 0))

				if event.key == pygame.K_p :
					pygame.image.save(WIN , "flipper.png")

				if event.key == pygame.K_j :
					r.body.apply_impulse_at_local_point(Vec2d.unit() * 40000 , ( 100 , 0))

				if event.key == pygame.K_b :
					mass = 1
					radius = 25
					inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
					body = pymunk.Body(mass, inertia)
					x = random.randint(115, 350)
					body.position = x, 200
					shape = pymunk.Circle(body, radius, (0, 0))
					shape.elasticity = elasticity
					space.add(body, shape)
					balls.append(shape)

		### Remove any balls outside
		to_remove = []
		for ball in balls:
			if ball.body.position.get_distance((300, 300)) > 1000:
				to_remove.append(ball)

		for ball in to_remove:
			space.remove(ball.body, ball)
			balls.remove(ball)

if __name__ == '__main__':
	main()