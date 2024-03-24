import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
class board():
	def __init__(self,score=0,children=None,depth=0,turn=True):
		self.score = score
		self.children = children
		self.depth=depth
		self.turn=0
		self.move=move
	def summative_score(self):
		while self.depth<3:
			for c in self.children:
				self.score+=self.summative_score(c)
			return self.score
	def create_children(self):
		pass
		
		

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

# Begninning of AI bot functions
# Bot function finds the best column to put the next piece
def bot():
	# Finds the valid placement options
	valid_locations = []
	for col in range(0, COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	# print(valid_locations)
	
	# Using the valid placement options, find the best option using score
	top_score = 0
	best_col = 0

	for i in valid_locations:
		temp_score = get_score(board, i)
		print(temp_score)
		if temp_score >= top_score:
			top_score = temp_score
			best_col = i
	
	return best_col

def get_score(board, col):
	# Creating a temporary board, calculate score
	# Dropping the piece onto the temporary board
	score = 0
	temp_board = board.copy()
	row = get_next_open_row(temp_board, col)
	drop_piece(temp_board, row, col, 2)

	# ------- Calculate the top score -------

	# Prioritize middle
	if col == 3:
		score += 5
	elif col == 2 or col == 4:
		score += 4
	elif col == 1 or col == 5:
		score += 3
	
  # Blocking
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if temp_board[r][c] == 1 and temp_board[r][c+1] == 1 and temp_board[r][c+2] == 1 and r == row and c+3 == col or (r == row and c == col and temp_board[r][c+1] == 1 and temp_board[r][c+2] == 1 and temp_board[r][c+3] == 1):
				score += 500
				
	for c in range(COLUMN_COUNT-2):
		for r in range(ROW_COUNT):
			if temp_board[r][c] == 1 and temp_board[r][c+1] == 1 and r == row and c+2 == col:
				score += 100

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if temp_board[r][c] == 1 and temp_board[r+1][c] == 1 and temp_board[r+2][c] == 1 and r+3 == row and c == col:
				score += 500

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if temp_board[r][c] == 1 and temp_board[r+1][c+1] == 1 and temp_board[r+2][c+2] == 1 and r+3 == row and c+3 == col:
				score += 500

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if temp_board[r][c] == 1 and temp_board[r-1][c+1] == 1 and temp_board[r-2][c+2] == 1 and r-3 == row and c+3 == col:
				score += 500

	# 4 in a row
	if winning_move(temp_board, 2):
		score += 1000

	# 3 in a row
	for c in range(COLUMN_COUNT-2):
		for r in range(ROW_COUNT):
			if temp_board[r][c] == 2 and temp_board[r][c+1] == 2 and temp_board[r][c+2] == 2:
				score += 50
				
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-2):
			if temp_board[r][c] == 2 and temp_board[r+1][c] == 2 and temp_board[r+2][c] == 2:
				score += 50
				
	for c in range(COLUMN_COUNT-2):
		for r in range(ROW_COUNT-2):
			if temp_board[r][c] == 2 and temp_board[r+1][c+1] == 2 and temp_board[r+2][c+2] == 2:
				score += 50

	for c in range(COLUMN_COUNT-2):
		for r in range(3, ROW_COUNT):
			if temp_board[r][c] == 2 and temp_board[r-1][c+1] == 2 and temp_board[r-2][c+2] == 2:
				score += 50
			
	# 2 in a row
	for c in range(COLUMN_COUNT-1):
		for r in range(ROW_COUNT):
			if temp_board[r][c] == 2 and temp_board[r][c+1] == 2:
				score += 25
				
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-1):
			if temp_board[r][c] == 2 and temp_board[r+1][c] == 2:
				score += 25
	
	for c in range(COLUMN_COUNT-1):
		for r in range(ROW_COUNT-1):
			if temp_board[r][c] == 2 and temp_board[r+1][c+1] == 2:
				score += 25
				
	for c in range(COLUMN_COUNT-1):
		for r in range(3, ROW_COUNT):
			if temp_board[r][c] == 2 and temp_board[r-1][c+1] == 2:
				score += 25

	return score

board = create_board()
# print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

				
			# AI Begins to play
			# turn == AI:				

			# Minimax and Alpha Beta Pruning to find the best col 
			#elif turn == AI:
			if game_over == False: 
				pygame.time.wait(100)
				col = bot()
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
						label = myfont.render("The AI wins!!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True

			# print_board(board)
			draw_board(board)

			# turn += 1
			# turn = turn % 2

			if game_over:
				pygame.time.wait(2000)