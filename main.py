from rushhour.classes.board import Board
from rushhour.classes.memory import Memory
from rushhour.visualisation.UserInterface import *

# set the board size and game number to load a specific puzzle
size = 6
game = 3

# create the file path for the chosen gameboard
board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"

memory = Memory()                       # initialize memory class
board = Board(f'{board_file}', size)    # initialize board 

# starts the user interface for selecting and running algorithms 
visualize_and_solve(board, memory)