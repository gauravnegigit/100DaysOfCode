import pygame
import math
pygame.font.init()

# main constants
WIDTH , HEIGHT = 800  , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Planet simulation")
FPS = 60

# color constants
WHITE = (255 , 255 , 255)
YELLOW = (255 , 255 , 0)
BLUE = (0 , 0 , 255)
RED = (255 , 0 , 0)
GREEN = (0 , 255 , 0)
BLACK = (0,0,0)
DARK_GREY = (80 , 78 , 80)

# font constants
FONT = pygame.font.SysFont("comicsans" , 20)

class Celestial :
	
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 250 / AU 
	TIMESTEP = 86400 # representing number of seconds in 1 day 

	def __init__(self , x , y , radius , color , mass) -> None:
		self.x = x 
		self.y = y 
		self.radius = radius 
		self.color = color 
		self.mass = mass 

		self.orbit = []
		self.sun = False 
		self.distance_to_sun = 0 

		self.x_vel = 0 
		self.y_vel = 0 
	
	def draw(self , win):
		x = self.x * self.SCALE + WIDTH /2
		y = self.y * self.SCALE + HEIGHT /2 
		pygame.draw.circle(win , self.color , (x , y) , self.radius)


		# code for drawing the orbits 
		if len(self.orbit) > 5 :
			new_points = []
			for point in self.orbit :
				x , y = point 
				x = x * self.SCALE + WIDTH /2
				y = y * self.SCALE + HEIGHT /2
				new_points.append((x , y))
			
			pygame.draw.lines(win , self.color , False , new_points , 2 )

	def attraction(self , other):
		other_x , other_y = other.x , other.y 
		distance_x = other_x - self.x 
		distance_y = other_y - self.y 
		distance = math.sqrt(distance_x**2 + distance_y **2)

		# if the other is sun then calulate the force 
		if other.sun :
			self.distance_to_sun = distance 

		# calculating the force using Newton's gravitational law
		force = self.G * self.mass * other.mass / distance**2

		theta = math.atan2(distance_y , distance_x)
		force_x = math.cos(theta) * force 
		force_y = math.sin(theta) * force 
		return force_x , force_y 
	
	def update_position(self , planets) :
		total_fx = total_fy = 0 

		for planet in planets :
			if self == planet :
				continue 
			fx , fy = self.attraction(planet)
			total_fx += fx 
			total_fy += fy 
		
		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		# updating x and y 
		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP 

		# updating orbits 
		self.orbit.append((self.x , self.y))

def main():
	run = True
	clock = pygame.time.Clock()

	sun = Celestial(0 , 0 , 50 , YELLOW , 1.98892 * 10**30)
	sun.sun = True 

	mercury = Celestial(-0.387 * Celestial.AU , 0 , 8 , DARK_GREY , 3.30 * 10**23)
	venus = Celestial(-0.723 * Celestial.AU , 0 , 14 , WHITE , 4.8685 * 10**24)
	earth = Celestial(-1 * Celestial.AU , 0 , 16 , BLUE , 5.9742 * 10**24)
	mars = Celestial(-1.524 * Celestial.AU , 0 , 12 , RED , 6.39 * 10**23)

	# initializing velocities of the plantes for initial momentum and causing circular motion due to centripetal force 
	mercury.y_vel = -47.4 * 1000
	venus.y_vel  = -35.02 * 1000
	earth.y_vel = -29.783 * 1000
	mars.y_vel = -24.077 * 1000

	planets = [sun , mercury , venus , earth , mars]

	while run :
		clock.tick(FPS)

		WIN.fill(BLACK)
		
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				run = False 
				pygame.quit()
				quit()
		
		for planet in planets :
			planet.update_position(planets)
			planet.draw(WIN)
		
		pygame.display.update()

if __name__ == "__main__" :
	main()