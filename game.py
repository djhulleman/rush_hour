from models import *
from data import *
import random

# select board size and game
size = 6
game = 1

# Create data process 
data = Data()

# create game board
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

def solve(board):
    '''algarithem that takes rendom steps to solve the puzzle'''
    # create object for car that needs to get out
    XX = board.cars["X"] 
    complete = False
    n = 0
    # Prevent infinite loops
    max_iterations = 10000000

    while not complete and n < max_iterations:
        # chose rendom car and rendom direction
        random_car = random.choice(list(board.cars.keys()))  
        random_move = random.choice([1, 2])
        # move the car if possible
        board.move(random_car, random_move) 
        n += 1
        print(f"Move {n}: Car {random_car} moved {'left/up' if random_move == 1 else 'right/down'}")

        # The "X" car is one step before the exit and the final position is empty
        if XX.col == board.size - 2 and board.board[XX.row - 1][board.size - 1] == '_':
            complete = True

    if complete:
        print(f"Puzzle solved in {n} moves!")
        board.print()
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")

solve(board)
data.export_moves()