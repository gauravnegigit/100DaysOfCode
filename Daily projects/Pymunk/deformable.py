import random
import pygame 
import pymunk 
import pymunk.autogeometry
import pymunk.pygame_util
from pymunk import BB

pygame.init()


# screen constants
WIDTH , HEIGHT = 600 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("DERFORMABLE")
FPS = 60 

# attributes 
elasticity = 1.009 

	

def draw_text():
	font = pygame.font.SysFont("Arial Black" , 16)
	text = [
		"Hold to draw pink color" , 
		"Hold + Shift to create balls" , 
		"Press g to genereate segements from pink color drawing " , 
		"Press r to reset"
	]

	y = 10
	for line in text :
		t = font.render(line , 1 , pygame.Color("black"))
		WIN.blit(t , (10 , y))
		y += 15 



def generate_geometry(surface , space):
	"""This function is used to generate the geometrical figures formed by pressing key 'g'"""

	for s in space.shapes :
		if hasattr(s , "generated") and s.generated :
			space.remove(s)

	def func(point):
		try :
			p = int(point[0]) , int(point[1])
			color = surface.get_at(p)
			return color.hsla[2] # using lightness 

		except Exception as e :
			print(e)
			return 0 

	lines = pymunk.autogeometry.march_soft(BB(0 , 0 , WIDTH - 1 , HEIGHT -1 ) , 60 , 60 , 90 , func)

	for line in lines :
		l = pymunk.autogeometry.simplify_curves(line , 1.0)

		for i in range(len(l) - 1):
			shape = pymunk.Segment(space.static_body , l[i] , l[i + 1] , 1)
			shape.friction = 0.5
			shape.color = pygame.Color("blue")
			shape.elasticity = elasticity
			shape.generated = True 
			space.add(shape)


def main():
	run = True 
	clock = pygame.time.Clock()

	# pymunk varaibles for physics stuff
	space = pymunk.Space()
	space.gravity = (0 , 981)
	draw_options = pymunk.pygame_util.DrawOptions(WIN)
	dt = 1/FPS


	# creating static lines 
	static_lines = [
		pymunk.Segment(space.static_body, (0, -50), (-50, 650), 5),
		pymunk.Segment(space.static_body, (0, 650), (650, 650), 5),
		pymunk.Segment(space.static_body, (650, 650), (650, -50), 5),
		pymunk.Segment(space.static_body, (-50, -50), (650, -50), 5),
	]

	for s in static_lines :
		s.collision_type = 1

	space.add(*static_lines)

	def pre_solve(arb , space , data):
		s = arb.shapes[0]
		space.remove(s.body , s)
		return False 

	space.add_collision_handler(0 , 1).pre_solve = pre_solve

	surface = pygame.Surface((600 , 600))
	surface.fill((255 , 255 , 255))

	# color for genrating shapes
	color = pygame.Color("green")
	pygame.draw.circle(surface , color , (450 , 100) , 100)
	generate_geometry(surface , space)


	# assigning few attributes to the default circle

	for i in range(25):
		mass = 1
		moment = pymunk.moment_for_circle(mass , 0 , 10)
		body = pymunk.Body(mass , moment)
		body.position = 450 , 100
		shape = pymunk.Circle(body , 10)
		shape.friction = 0.5
		shape.elasticity = elasticity
		space.add(body , shape)

	pymunk.pygame_util.positive_y_is_up = False

	while run :
		clock.tick(FPS)
		space.step(dt)
		WIN.blit(surface , (0 , 0))
		draw_text()
		space.debug_draw(draw_options)

		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False
				pygame.quit()
				quit()

			elif event.type == pygame.KEYDOWN :
				if event.key == pygame.K_g :
					generate_geometry(surface , space)

				if event.key == pygame.K_p :
					pygame.image.save(WIN , "deformable.png")

				elif event.key == pygame.K_r :
					surface.fill((255 , 255 , 255))
					for s in space.shapes :
						if hasattr(s , "generated") and s.generated:
							space.remove(s)
					main()


		if pygame.mouse.get_pressed()[0]:
			if pygame.key.get_mods() and pygame.KMOD_SHIFT :
				body = pymunk.Body(mass , moment)
				body.position = pygame.mouse.get_pos()
				shape = pymunk.Circle(body , 10)
				shape.friction = 0.5 
				shape.elasticity = elasticity
				space.add(body , shape)

			else :
				color = pygame.Color("green")
				pos = pygame.mouse.get_pos()
				pygame.draw.circle(surface , color , pos , 25)

		pygame.display.update()

if __name__ == '__main__':
	main()