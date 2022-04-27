import os
from colorama import Fore , init 
from pytimedinput import timedInput
import random

# initializing colorama 
init(autoreset = True )

# main constants 
WIDTH , HEIGHT = 35 , 20
CELLS = [(col , row) for row in range(HEIGHT) for col in range(WIDTH)]


def print_field():
	for cell in CELLS:
		if cell in snake_body:
			print(Fore.GREEN + 'X', end = '')
		elif cell == apple_pos:
			print(Fore.RED + 'O',end = '')
		elif cell[1] in (0, HEIGHT - 1) or cell[0] in (0, WIDTH - 1):
			print(Fore.CYAN + '#', end = '')
		else:
			print(' ', end = '')

		if cell[0] == WIDTH - 1:
			print('')

def update_snake():
	global eaten

	new_head = snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]
	snake_body.insert(0,new_head)
	if not eaten:
		snake_body.pop(-1)
	eaten = False

def apple_collision():
	global apple_pos, eaten

	if snake_body[0] == apple_pos:
		apple_pos = apple()
		eaten = True 

def apple():
	x , y = random.randint(1 , WIDTH - 2) , random.randint(1 , HEIGHT - 2)

	while (x , y) in snake_body :
		x , y = random.randint(1 , WIDTH - 2) , random.randint(1 , HEIGHT - 2)

	return (x , y)


# game variabless
# snake body 

snake_body = [(5,HEIGHT // 2),(4,HEIGHT // 2),(3,HEIGHT // 2)]
DIRECTIONS = {'left' : (-1 , 0) , 'right' : (1 , 0) , 'up' : (0 , -1) , 'down' : (0 , 1)}
direction  = DIRECTIONS['right']
apple_pos = apple()
eaten = False 


while True :
	os.system('cls')

	# drawing the field 
	print_field()

	# get input 
	txt , ret = timedInput('' , timeout = 0.3)

	
	if txt == 'w':
		direction = DIRECTIONS['up']
	elif txt == 'a' :
		direction = DIRECTIONS['left']
	elif txt == 's' :
		direction = DIRECTIONS['down']
	elif txt == 'd' :
		direction = DIRECTIONS['right']
	
	elif txt == 'q' :
		os.system('cls')
		quit()


	# updating teh game 
	update_snake()
	apple_collision()

	# check death 
	if snake_body[0][1] in (0 , HEIGHT - 1) or snake_body[0][0] in (0 , WIDTH - 1) or snake_body[0] in snake_body[1:] :
		os.system('cls')
		break 
