from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.visualisation.plot_solutions import plot_solution
from rushhour.algorithms.random_with_memory import *
from rushhour.algorithms.random_with_plot import solve_with_visualization
from rushhour.algorithms.improve_solution import *


size = 6
game = 1

board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"

# Create data processes
data = Data()
memory = Memory()
# create game board
board = Board(f'{board_file}', size, data)

random_with_memory(board, memory)
board.data.export_moves('solutions/output.csv')
solve_with_visualization(board)


solution_file = "solutions/output.csv"
plot_solution(board_file, solution_file)