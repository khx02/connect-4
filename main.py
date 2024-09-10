import random

ROWS = 6
COLUMNS = 7 


def validate_input(prompt, valid_inputs):
	"""
	Repeatedly ask user for input until they enter an input
	within a set valid of options.
	:param prompt: The prompt to display to the user, string.
	:param valid_inputs: The range of values to accept, list
	:return: The user's input, string.
	"""

	while True:
		user_input = input(prompt)
		if user_input in valid_inputs: # checks if user input is within range of valid inputs
			return user_input
		print("Invalid input, please try again.") # continues looping if not

def create_board():
	"""
	Returns a 2D list of 6 rows and 7 columns to represent
	the game board. Default cell value is 0.
	:return: A 2D list of 6x7 dimensions.
	"""

	board_ls = [] #creates an empty list to store all rows formed, creating the board
	for i in range(ROWS): #defining how many rows to create
		row_ls = [] # creates an empty row list to store the number of cell in a column, creating a row
		for n in range(COLUMNS): # defining how many cells each row contains
			row_ls.append(0) # for each row list created, it appends a column's worth of zeroes into that row
		board_ls.append(row_ls) # all the rows containing the zeroes will then be stored inside one list row
	return board_ls

def print_board(board):
	"""
	Prints the game board to the console.
	:param board: The game board, 2D list of 6x7 dimensions.
	:return: None
	"""

	print("========== Connect4 =========")
	print("Player 1: X", "     ", "Player 2: O")
	print("")

	#printing header numbers for columns
	for column in range(1, COLUMNS + 1):
		print(" ", column, "", end="")

	print("\n", end="") # enter into the next line for the rows

	for row in range(ROWS):
		for dashes in range(COLUMNS):
			print("", "---", end= "") # prints the top border of the board and horizontal lines inside the board
		print("\n", end="")

		for col in range(COLUMNS): # creating the cells inside the row
			if board[row][col] == 1:
				print("| X ", end= "") # prints player symbol if there is one, if not prints a space
			elif board[row][col] == 2:
				print("| O ", end= "")
			else:
				print("|   ", end="") # prints the left border of the board as well as the vertical lines inside the board

		print("|\n", end="") # prints the right border of the board

	print(" --- --- --- --- --- --- ---") # prints the bottom border of the board
	print("=============================") # prints the footer of the connectK board

def drop_piece(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.
	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: True if piece was successfully dropped, False if not.
	"""
	#check if the column is filled 
	for row in range(ROWS - 1, -1, -1): # checks each row from bottom to top
	# ROWS - 1 to get index value of most bottom row
	# -1 to end before -1, hence 0
	# -1 because going from bot to top, hence decreasing row number
		if board[row][column-1] == 0:
			board[row][column-1] = player # checks if cell is available and assign player number to it, returns true afterwards
			return True
	return False

def execute_player_turn(player, board):
	"""
	Prompts user for a legal move given the current game board
	and executes the move.
	:return: Column that the piece was dropped into, int.
	"""
	while True:	
		# ask the user for the column number to place their token in, if that column is available, it will drop the token in that column. if not available, it will prompt again. if column is not valid (out of range), it will also prompt again
		prompt =  "Player " + str(player)+ " please enter the column you would like to drop your piece into: "
		user_input = validate_input(prompt, ["1", "2", "3", "4", "5", "6", "7"])
		if drop_piece(board, player, int(user_input)) == True:
			return int(user_input)
		else:
			print("That column is full, please try again.")

def end_of_game(board): 
	"""
	Checks if the game has ended with a winner
	or a draw.
	:param board: The game board, 2D list of 6 rows x 7 columns.
	:return: 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if draw.
	"""

	def winner(player):

		# - horizontal check
		for row in range(ROWS): # iterates through each row
			for column in range(COLUMNS - 3): # iterates through columns required
				if all(board[row][column + i] == player for i in range(4)): # checks if 4 in a row
					return True

		# | vertical check	
		for column in range(COLUMNS): #iterates through each columns
			for row in range(ROWS - 3): #checks the top 3 rows of each column
				if all(board[row + i][column] == player for i in range(4)):
					return True

		# \ top left to bottom right check
		for row in range(ROWS - 3): # diagonal 4 piece is only possible from row 3 col 1-4
			for column in range(COLUMNS - 3):
				if all(board[row + i][column + i] == player for i in range(4)):
					return True
		# / top right to bottom left check	
		for row in range(ROWS - 3): # diagonal 4 piece is only possible from row 3 col 4-7
			for column in range(3, COLUMNS): 
					if all(board[row + i][column - i] == player for i in range(4)):
						return True
		return False

	if winner(1): #check if player 1 wins
		return 1
	elif winner(2): #check if player 2 wins
		return 2

	for row in board:	#check if the game is drawn
		for cell in row:
			if cell == 0:
				return 0	#there's still empty cells, game is not drawn
		else:
			return 3	 


def clear_screen():
	"""
	Clears the terminal for Windows and Linux/MacOS.
	:return: None
	"""
	import os
	os.system('cls' if os.name == 'nt' else 'clear')


def local_2_player_game():
	"""
	Runs a local 2 player game of Connect 4.
	:return: None
	"""
	current_player = 1 # first player is always player 1
	board = create_board()
	game_state = 0
	last_dropped = 0
	game_turn = 0 

	while game_state == 0: # game will continue if there's no winner nor draw
		clear_screen()
		print_board(board)
		if game_turn != 0: # will not prompt if it's the first move of the game
			print("Player",str(3 - current_player),"dropped a piece into column", str(last_dropped)) # displays the previous player's move
		last_dropped = execute_player_turn(current_player, board)
		game_state = end_of_game(board) # checking if there's a win
		game_turn = 1
		current_player = 3 - current_player # current_player will be either 1 or 2

	if game_state == 1: # player 1 wins
		clear_screen()
		print_board(board)
		print("Congratulations Player 1! You've won!")
	elif game_state == 2: # player 2 wins
		clear_screen()
		print_board(board)
		print("Congratulations Player 2! You've won!")
	else: # draw
		clear_screen()
		print_board(board)
		print("This game is a tie!")


def cpu_player_easy(board, player):
	"""
	Executes a move for the CPU on easy difficulty. This function
	plays a randomly selected column.
	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""
	while True:
		random_col = random.randint(1, COLUMNS) # chooses a random column between 1 and 7
		if drop_piece(board, player, random_col) == True: # checks if that column is available, and drops it
			return random_col

def print_rules():
	"""
	Prints the rules of the game.
	:return: None
	"""
	print("================= Rules =================")
	print("Connect 4 is a two-player game where the")
	print("objective is to get four of your pieces")
	print("in a row either horizontally, vertically")
	print("or diagonally. The game is played on a")
	print("6x7 grid. The first player to get four")
	print("pieces in a row wins the game. If the")
	print("grid is filled and no player has won,")
	print("the game is a draw.")
	print("=========================================")

def print_main_menu():
	"""
	Print the main menu.
	:return: None
	"""
	print("=============== Main Menu ===============")
	print("Welcome to Connect 4!")
	print("1. View Rules")
	print("2. Play a local 2 player game")
	print("3. Play a game against the computer")
	print("4. Exit")
	print("=========================================")

def main():
	"""
	Main function of the program. This function is called when the program
	is run.
	:return: None
	"""
	clear_screen()
	user_input = 0
	while user_input != 4: # will keep prompting unless player wants to exit
		print_main_menu()
		user_input = int(validate_input("Please select an option (1, 2, 3, 4):", ["1", "2", "3", "4"]))
		if user_input == 1: # view rules
			clear_screen()
			print_rules()
		elif user_input == 2: # local 2 player game
			local_2_player_game()
		elif user_input == 3:
			game_against_cpu() # play against computer
		else:
			break # exit


def cpu_player_medium(board, player):
	"""
	Executes a move for the CPU on medium difficulty.
	It first checks for an immediate win and plays that move if possible.
	If no immediate win is possible, it checks for an immediate win
	for the	opponent and blocks that move. If neither of these are
	possible, it plays a random move.
	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""
	OPPONENT = 3 - player

	'''
	creates a temporary board to simulate dropping a token. if it results in a win for that player, then it drops it in the actual board to win the game
	'''
	for column in range(1, COLUMNS + 1): # simulates dropping in every column
		temp_board = [row[:] for row in board]
		if drop_piece(temp_board, player, column) and end_of_game(temp_board) == player: 
			drop_piece(board, player, column)
			return column

	'''
	creates a temporary board to simulate dropping a token as the opponent. if it results in a win for the opponent, then it the player drops it in the actual board and blocks the winning move
	'''
	for column in range(1, COLUMNS + 1): # simulates dropping in every column
		temp_board = [row[:] for row in board]
		if drop_piece(temp_board,	OPPONENT, column) and end_of_game(temp_board) == OPPONENT:
			drop_piece(board, player, column)
			return column

	'''
	if no winning move or blocking move was found, then the player would drop the token in a random column
	'''
	random_col = cpu_player_easy(board, player)
	return random_col


def cpu_player_hard(board, player):
	"""
	Executes a move for the CPU on hard difficulty.
	cpu_player_hard uses a scoring mechanism to determine the best column to drop the token in:
	- It first creates a temporary board and simulates dropping a token into a column.
	- It will then give a score to that column based on how 'winnable' that column is.
	- The score wll be based on a variety of factors:
		- if the column that the token is dropped in results in 3 in a row
		- if the column that the token is dropped in results in 2 in a row
		- if the column that the token is dropped in will neglect a winning move for the 	 
		  opponent
		- if the column that the token is dropped in will neglect a 2 in a row for the 
		  opponent
		- tokens in the column center would have a higher score than the others
	- This process will repeat for every column
	- After scoring every column, the column with that results in an immediate win or the highest score will be the one that the 
	  token is dropped in in the actual board
	cpu_player_hard is also able to predict if the move they played will result in the opponent winning in the next move and avoid it:
	- The initial scoring mechanism doesn't suffice as it can only block the winning move
	- It first creates another temporary board of the initial temporary board with the simulated move in it
	- It will then simulate dropping the token into each column as the opponent and checking if it results in the opponent winning
	- If the opponent does win, it will avoid playing that move and move on to the next column
	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: None
	"""
	OPPONENT = 3 - player

	def get_window_score(window, player):
		"""
		Counts the number of 2s and 3s in a row for each column.
		We give a higher score for 3s in a row than 2s in a row.
		Negative score will be given if winning move or 2s in a row for the opponent is neglected
		We give a higher negative score for neglecting winning move than 2s in a row
		:param window: A list of 4 integers representing a window of 4 consecutive spaces on the board.
		:param player: The player whose turn it is, integer value of 1 or 2.
		:return: The score for the window, int.
		"""
		score = 0

		if window.count(player) == 3 and window.count(0) == 1: # 3 in a row with 1 empty space
			score += 500
		elif window.count(player) == 2 and window.count(0) == 2: # 2 in a row with 2 empty spaces
			score += 90

		if window.count(OPPONENT) == 3 and window.count(0) == 1: # opponent has 3 in a row with 1 empty space
			score -= 9000
		if window.count(OPPONENT) == 2 and window.count(0) == 2: # opponent has 2 in a row with 2 empty spaces
			score -=200


		return score

	def column_score(board, player): 
		"""
		Scores the current position on the board.
		:param board: The game board, 2D list of 6x7 dimensions.
		:param player: The player whose turn it is, integer value of 1 or 2.
		:return: The score for the position, int.
		"""
		score = 0
		center = [board[i][3] for i in range(ROWS)] #creates a list of the pieces in the center column
		center_count = center.count(player) #counts the number of pieces in the center column
		score += center_count * 95 # gives a higher score for pieces in the center column

		# -
		for row in range(ROWS): #checks each row
			for col in range(COLUMNS - 3): #checks each window of 4 consecutive spaces
				window = [board[row][col + i] for i in range(4)] #creates a list of 4 consecutive spaces
				score += get_window_score(window, player) 

		# |
		for col in range(COLUMNS): #checks each column
			for row in range(ROWS - 3): #checks each window of 4 consecutive spaces
				window = [board[row + i][col] for i in range(4)] 
				score += get_window_score(window, player)

		# /
		for row in range(ROWS - 3): #checks each top right to bottom left diagonal
			for col in range(COLUMNS - 3):
				window = [board[row + i][col + i] for i in range(4)] 
				score += get_window_score(window, player)
		# \
		for row in range(ROWS - 3): #checks each top left to bottom right diagonal
			for col in range(COLUMNS - 3):
				window = [board[row + 3 - i][col + i] for i in range(4)]
				score += get_window_score(window, player)

		return score


	best_score = -10000000 # score set to negative as we always want the first score to be best score (if set to 0 but all columns scores are negative, then logic error)
	best_col = 0
	for c in range(1, COLUMNS + 1): # iterating through each and every column
		lose = False
		temp_board = [row[:] for row in board] # creates a temporary board
		if drop_piece(temp_board, player, c) and end_of_game(temp_board): # simulates dropping the token in given column. if drop successfull and win, drop in actual board
			drop_piece(board, player, c)
			return c
		temp_board = [row[:] for row in board] # creates a new temp_board because previous one already has the simulated token
		if drop_piece(temp_board, player, c):
			score = column_score(temp_board, player) # if successfull drop, score the columns
			for c_opp in range(1, COLUMNS + 1): # simulates dropping as opponent in every column
				temp_opp_board = [row[:] for row in temp_board] # have to create another temp board for the temp board because we are dropping multiple times
				if drop_piece(temp_opp_board, OPPONENT, c_opp) and end_of_game(temp_opp_board): # simulates dropping the token in the given column, if successfull and win as opponent, we would want to avoid that column
					lose = True
			if not lose and score > best_score:
				best_score = score
				best_col = c

	drop_piece(board, player, best_col)
	return best_col

def clear_screen():
	"""
	Clears the terminal for Windows and Linux/MacOS.
	:return: None
	"""
	import os
	os.system('cls' if os.name == 'nt' else 'clear')


def game_against_cpu():
	"""
	Runs a game of Connect 4 against the computer.
	:return: None
	"""
	board = create_board()
	difficulty = int(validate_input("Choose the CPU difficulty: (1:Easy, 2:Medium, 3:Hard): ", ["1", "2", "3"]))

	game_state = 0 # 0 = game in progress, 1 = player wins, 2 = CPU wins, 3 = draw
	move_human = 0 # stores the column number of the last move made by the human player
	move_cpu = 0 # stores the column number of the last move made by the CPU
	while game_state == 0:
		clear_screen() 
		print_board(board) 
		if move_human != 0:
			print("You dropped a piece into column", move_human)
		if move_cpu != 0:
			print("CPU dropped a piece into column",  move_cpu)
		# human move
		move_human = execute_player_turn(1, board) # player 1 is the human player
		game_state = end_of_game(board) # checks if the game has ended
		if game_state == 1: #player 1 wins
			clear_screen() 
			print_board(board) 
			print("Congratulations Player 1! You've won!")
		elif game_state == 3: #draw
			clear_screen()
			print_board(board)
			print("This game is a tie!")
		# cpu turn # player 2 is the CPU
		if difficulty == 1:
			move_cpu = cpu_player_easy(board, 2) 
		elif difficulty == 2:
			move_cpu = cpu_player_medium(board, 2) 
		else:
			move_cpu = cpu_player_hard(board, 2)
		game_state = end_of_game(board) # checks if the game has ended
		if game_state == 2: #player 2 wins
			clear_screen()
			print_board(board)
			print("The CPU has won!")
		elif game_state == 3: #draw
			clear_screen()
			print_board(board)
			print("This game is a tie!")


if __name__ =="__main__":
	main()