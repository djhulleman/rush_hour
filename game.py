from models import *
from board import *
import random


# create game board and show it
board = Board('gameboards/Rushhour12x12_7.csv', 12)

import random

def solve(board):
    XX = board.cars["X"] 
    complete = False
    n = 0
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(list(board.cars.keys()))  
        random_move = random.choice([1, 2])

        # Check if the move is valid

        board.move(random_car, random_move) 
        n += 1
        print(f"Move {n}: Car {random_car} moved {'left/up' if random_move == 1 else 'right/down'}")

        # Check if the "X" car has reached the exit
        if XX.col + XX.length - 1 == board.size:
            complete = True
        # The "X" car is one step before the exit and the final position is empty
        elif XX.col == board.size - 2 and board.board[XX.row - 1][board.size - 1] == '_':
            complete = True

    if complete:
        print(f"Puzzle solved in {n} moves!")
        board.print()
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")





solve(board)