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
		

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def tie_game(board):
	tie_game=True
	for y in board:
		for x in y:
			if x<1:
				tie_game=False
	return tie_game

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

def valid_columns(board):
	valid_locations = []
	for col in range(0, COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

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
		temp_board = board.copy()
		row = get_next_open_row(temp_board, i)
		drop_piece(temp_board, row, i, 2)
		temp_score = get_score(temp_board, 2, 1)
		print(temp_score)
		if temp_score >= top_score:
			top_score = temp_score
			best_col = i
	
	return best_col

def get_score(board, piece, other_piece):
	# Creating a temporary board, calculate score
	# Dropping the piece onto the temporary board
	score = 0
	# ------- Calculate the top score -------
	# Prioritize middle
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and c == 2:
				score += 25
			if board[r][c] == piece and (c == 2 or c == 4):
				score += 15
			if board[r][c] == piece and (c == 1 or c == 5):
				score += 10
				

  # Blocking
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == other_piece and board[r][c+1] == other_piece and board[r][c+2] == other_piece and r == row and c+3 == col or (r == row and c == col and board[r][c+1] == other_piece and board[r][c+2] == other_piece and board[r][c+3] == other_piece):
				score += 1000
				
	for c in range(COLUMN_COUNT-2):
		for r in range(ROW_COUNT):
			if board[r][c] == other_piece and board[r][c+1] == other_piece and r == row and c+2 == col:
				score += 1000

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == other_piece and board[r+1][c] == other_piece and board[r+2][c] == other_piece and r+3 == row and c == col:
				score += 1000

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == other_piece and board[r+1][c+1] == other_piece and board[r+2][c+2] == other_piece and r+3 == row and c+3 == col:
				score += 1000

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == other_piece and board[r-1][c+1] == other_piece and board[r-2][c+2] == other_piece and r-3 == row and c+3 == col:
				score += 1000

	# 4 in a row
	if winning_move(board, 2):
		score += 10000

	# 3 in a row
	for c in range(COLUMN_COUNT-2):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece:
				score += 50
				
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-2):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece:
				score += 50
				
	for c in range(COLUMN_COUNT-2):
		for r in range(ROW_COUNT-2):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece:
				score += 50

	for c in range(COLUMN_COUNT-2):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece:
				score += 50
			
	# 2 in a row
	for c in range(COLUMN_COUNT-1):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece:
				score += 25
				
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-1):
			if board[r][c] == piece and board[r+1][c] == piece:
				score += 25
	
	for c in range(COLUMN_COUNT-1):
		for r in range(ROW_COUNT-1):
			if board[r][c] == piece and board[r+1][c+1] == piece:
				score += 25
				
	for c in range(COLUMN_COUNT-1):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece:
				score += 25
	print(score)
	return score


def terminal_board(board):
	return winning_move(board, 1) or winning_move(board, 2) or tie_game(board)


def minimax(board,depth,bot_turn):
	valid_locations = valid_columns(board)
	if depth==0 or terminal_board(board):
		if terminal_board(board):
			if winning_move(board, 1):
				return (None,-math.inf)
			elif winning_move(board, 2):
				return (None, math.inf)
			else:
				return (None, 0)
		else:
			return (None,get_score(board,1,2))
		
	elif bot_turn:
		value=-math.inf
		column=valid_locations[0]
		for col in valid_locations:
			row = get_next_open_row(board,col)
			temp=board.copy()
			drop_piece(temp, row, col, 2)
			total_score = minimax(temp, depth-1, False)[1]
			if total_score>value:
				value=total_score
				column=col
		return column, value
		
	elif not bot_turn:
		value = math.inf
		column=valid_locations[0]
		for col in valid_locations:
			row = get_next_open_row(board,col)
			temp=board.copy()
			drop_piece(temp, row, col, 1)
			total_score = minimax(temp, depth-1, True)[1]
			if total_score<value:
				value=total_score
				column=col
		return column, value



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
				col = minimax(board,4, True)[0]
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