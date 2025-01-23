from rushhour.classes.board import Board
from rushhour.classes.memory import Memory
from rushhour.visualisation.UserInterface import *
from rushhour.algorithms.Astar import *
from copy import deepcopy

size = 6
game = 1

board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"

# Create data processes
memory = Memory()

board = Board(f'{board_file}', size)
start = deepcopy(board )

visualize_and_solve(board, "solutions/output.csv")

("solutions/output.csv")
