
from rushhour.visualisation.UserInterface import *
from rushhour.classes.board import Board
from rushhour.visualisation.solution_gif import plot_solution_to_gif
# run userinterface te select the board and the algorithm
#UserInterface()

s = 6
g = 1
board = Board(f"gameboards/Rushhour{s}x{s}_{g}.csv", s)

plot_solution_to_gif(board, "solutions/A*/solutions6x6_1.csv")