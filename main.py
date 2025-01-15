from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.visualisation.plot_solutions import plot_solution
from rushhour.algorithms.random_with_memory import *
from rushhour.algorithms.random_with_plot import solve_with_visualization


size = 12
game = 7
# Create data process 
data = Data()
# create game board
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)


board_file = "gameboards/Rushhour6x6_1.csv"
solution_file = "solutions/solutions6x6_1.csv"
#plot_solution(board_file, solution_file)

finished = random_with_memory(board_file)

print(finished.data.output_data)
finished.data.export_moves()
#solve_with_visualization(board)


#solution_file = "output.csv"
#plot_solution(board_file, solution_file)