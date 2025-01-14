"""
This model can solve the games 6x6_1, 6x6_2, 6x6_3, 9x9,4, 9x9_5 en 9x9_6
Cannot solve 12x12_7 within an acceptable timespan
"""

from rushhour.classes.board import Board
from rushhour.classes.board import Car
from rushhour.classes.data import Data
import random
import copy

saved_boards =[]
cycles = []

data = Data()
    
def save_board(cars, saved_boards):
    cars_copy = {}
    for key, car in cars.items():
        car_copy = Car(
            car=car.car,
            orientation=car.orientation,
            col=car.col,
            row=car.row,
            length=car.length,
            color=car.color
        )

        cars_copy[key] = car_copy
    saved_boards.append(cars_copy)

def compare_board(previous_cars, current_car):

    # Now compare each car's important properties.
    for key in previous_cars:
        car1 = previous_cars[key]
        car2 = current_car[key]
        
        # Compare orientation, row, col, and length.
        if ( car1.row != car2.row or 
            car1.col != car2.col ):
            #print("No Setup similar")
            return False
    #print("similar setup found")
    return True


def compare_boards(saved_boards, current_cars):
    for i, previous_car in enumerate(saved_boards):
        if compare_board(previous_car, current_cars):
            return i
    return None

def create_board(board, size, position):
    # create matrix for board with all '_'
    board.board = [['_'] * size for _ in range(size)]

    # get car properties from saved_boards
    board.cars = copy.deepcopy(saved_boards[position])

    # add the cars to the board
    for CAR in board.cars:
        car = board.cars[CAR]
        # see what the orientation is of the car and print it accordingly
        if car.orientation == "H":
            for j in range(0, car.length):
                board.board[car.row-1][car.col+j-1] = car
        elif car.orientation == "V":
            for j in range(0, car.length):
                board.board[car.row+j-1][car.col-1] = car

sizee = 12
# create game board and show it
board = Board('gameboards/Rushhour12x12_7.csv', sizee, data)
save_board(board.cars, saved_boards)

def solve(board):
    XX = board.cars["X"]
    complete = False
    n = 0
    s = 0
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(list(board.cars.keys()))
        random_move = random.choice([1, 2])

        board.move(random_car, random_move)

        comparison_result = compare_boards(saved_boards, board.cars)
        if comparison_result is not None:
            n = comparison_result
            create_board(board, sizee, n)
            del saved_boards[n+1:]
            data.del_moves(n)
        else: 
            save_board(board.cars, saved_boards)
            n += 1
        s += 1


        complete = board.check_finish()
        if s%10000 == 0:
            print(f"loading, {s} steps")

    if complete:
        print(f"Puzzle solved in {n} moves!")
        board.print()
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")

solve(board)
data.export_moves()

# board.print()
# print("")

# board.move("A", 1)
# compare_boards(saved_boards, board.cars)
# if compare_boards(saved_boards, board.cars) == False:
#     save_board(board.cars, saved_boards)

# board.print()
# print("")

# board.move("A", 2)
# compare_boards(saved_boards, board.cars)
# if compare_boards(saved_boards, board.cars) == False:
#     save_board(board.cars, saved_boards)

# board.print()
# print("")

# create_board(board, 6, 1)

# board.print()