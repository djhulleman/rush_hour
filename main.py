from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.visualisation.plot_solutions import plot_solution
from rushhour.algorithms.random_with_memory import *
from rushhour.visualisation.dynamic_board_draw import draw_board_dynamic
from rushhour.visualisation.UserInterface import *


size = 6
game = 1
data = Data()
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

board.print()

visualize_and_solve(board)