from rushhour.classes.board import Board
from rushhour.classes.memory import Memory
from rushhour.visualisation.UserInterface import *
from rushhour.algorithms.IDS import *

size = 6
game = 1

board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"

# Create data processes
memory = Memory()

# create game board
board = Board(f'{board_file}', size)


solution = IDS(board)
solution.print()