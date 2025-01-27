from rushhour.classes.board import Board
from rushhour.classes.memory import Memory
from rushhour.visualisation.UserInterface import *
from rushhour.algorithms.Astar import *
from rushhour.visualisation.statespace import *
from copy import deepcopy

size = 9
game = 4

board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"

# Create data processes
memory = Memory()

board = Board(f'{board_file}', size)
start = deepcopy(board )


calculate_statespace(board_file, 9)
