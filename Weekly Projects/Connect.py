import pygame
import math
pygame.font.init()

# main screen variables
WIDTH , HEIGHT = (700 , 700)
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("CONNECT FOUR GAME USING PYGAME !")
FPS = 60

# game variables
SQUARESIZE = 100
ROWS = 6 
COLUMNS = 7
RADIUS = (SQUARESIZE - 10)//2

# color variables
BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0 )
BLUE = (0 ,0, 255)
YELLOW = (255 , 255 , 0)
WHITE = (255,255,255)

#font variables
FONT = pygame.font.SysFont("ARIAL BLACK" , 35)

def drop_piece(board , row , col , piece):
	board[row][col] = piece

def is_valid_position(board , col):
	return board[0][col] == 0

def get_next_row(board , col):
	for i in range(ROWS - 1, -1 , -1):
		if board[i][col] == 0 :
			return i

def isWinner(board, piece):
	# Horizontal cells check
	for i in range(COLUMNS - 3):
		for j in range(ROWS):
			if board[j][i] ==piece and board[j][i + 1] == piece and board[j][i + 2] == piece and board[j][i + 3] == piece : 
				return True

	#Vertical cells check 
	for i in range(COLUMNS):
		for j in range(ROWS - 3):
			if board[j][i] ==piece and board[j + 1][i] == piece and board[j + 2][i] == piece and board[j + 3][i] == piece : 
				return True

	# checking for diagonals in connect four 
	for i in range(COLUMNS - 3):
		for j in range(ROWS - 3):
			if board[j][i] ==piece and board[j + 1][i + 1] == piece and board[j + 2][i + 2] == piece and board[j + 3][i + 3] == piece : 
				return True

	for i in range(COLUMNS -3):
		for j in range(ROWS):
			if board[j][i] == piece and board[j - 1][i + 1] == piece and board[j - 2][i + 2] == piece and board[j - 3][i + 3] == piece :
				return True 

def redraw(board):

	WIN.fill(BLUE)

	for c in range(COLUMNS):
		for r in range(ROWS):
			pygame.draw.circle(WIN , BLACK , ((c* SQUARESIZE + SQUARESIZE//2) , ((r + 1) * SQUARESIZE + SQUARESIZE//2 )) , RADIUS)

	for c in range(COLUMNS):
		for r in range(ROWS):
			if board[r][c] == 1:
				pygame.draw.circle(WIN , RED , ((c* SQUARESIZE + SQUARESIZE//2) , ((r + 1)*SQUARESIZE + SQUARESIZE//2)) , RADIUS)

			if board[r][c] == 2:
				pygame.draw.circle(WIN , YELLOW , ((c* SQUARESIZE + SQUARESIZE//2) , ((r + 1)*SQUARESIZE + SQUARESIZE//2)) , RADIUS)

def reset_board():
	board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)] 
	return board 

def main():
	run = True
	clock = pygame.time.Clock()

	#turn of current player
	turn = 0 
	board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
	print(board)


	# main loop
	while run :
		clock.tick(FPS)

		redraw(board)
		pygame.draw.rect(WIN , BLACK ,(0 , 0 , WIDTH , SQUARESIZE ))
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				run = False
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEMOTION :
				posx = event.pos[0]

				if turn == 0 :
					pygame.draw.circle(WIN , RED , (posx , SQUARESIZE//2) , RADIUS)
				else :
					pygame.draw.circle(WIN , YELLOW , (posx , SQUARESIZE//2) , RADIUS)


			if event.type == pygame.MOUSEBUTTONDOWN :
				pygame.draw.rect(WIN , BLACK , (0,0 , WIDTH  , SQUARESIZE))

				posx = event.pos[0]
				col = posx//SQUARESIZE

				if is_valid_position(board , col):
					row = get_next_row(board , col)
					drop_piece(board , row, col , turn + 1)

				if turn == 0 :
					color = RED 
				else :
					color = YELLOW

				if isWinner(board , turn + 1):
					label = FONT.render(f"Player {(turn + 1)} wins !" , 1, color)

					redraw(board)
					pygame.draw.rect(WIN , BLACK ,(0 , 0 , WIDTH , SQUARESIZE ))
					WIN.blit(label , (40 , 10))
					pygame.display.update()
					run = False
					board = reset_board()
					pygame.time.delay(1500)

				turn += 1
				turn = turn % 2 

		pygame.display.update()


def main_menu():
	start = True 

	clock = pygame.time.Clock()
	while start :
		clock.tick(FPS)

		WIN.fill(BLACK)
		text = FONT.render("PRESS ANY KEY TO CONTINUE !" , 1 ,WHITE)
		WIN.blit(text , (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))

		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				start = False
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN :
				main()

		pygame.display.update()

main_menu()
