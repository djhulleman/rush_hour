import random
from rushhour.classes.board import Board
from rushhour.classes.car import Car
from rushhour.classes.data import Data

saved_boards =[]
board_hashes = {}
data = Data()

def hash_board(board_copy, car_names):
    cars_properties = []
    for key in car_names:
        r, c = board_copy[key]
        cars_properties.append(f"{key}:{r}:{c}")
    return "|".join(cars_properties)
    
def save_board(cars, saved_boards, board_hashes, car_names):
    board_copy = {}
    for key, car in cars.items():
        board_copy[key] = (car.row, car.col)
    
    saved_boards.append(board_copy)

    h = hash_board(board_copy, car_names)
    board_hashes[h] = len(saved_boards) - 1

def compare_boards(cars, board_hashes, car_names):
    current_board_copy = {}
    for key, car in cars.items():
        current_board_copy[key] = (car.row, car.col)

    h = hash_board(current_board_copy, car_names)
    return board_hashes.get(h, None)

def create_board(board, size, position):

    board.board = [['_'] * size for _ in range(size)]

    # Get car properties from saved_boards list 
    saved_board = saved_boards[position]

    # Update each car’s row and col 
    for car_name, (r, c) in saved_board.items():
        board.cars[car_name].row = r
        board.cars[car_name].col = c

    # Place the cars on the 2D matrix
    for car in board.cars.values():
        if car.orientation == "H":
            for j in range(car.length):
                board.board[car.row - 1][car.col + j - 1] = car
        else:  # orientation == "V"
            for j in range(car.length):
                board.board[car.row + j - 1][car.col - 1] = car

def random_with_memory(board):

    size = board.size
    data = Data()
    car_names = board.cars.keys()
    car_list = list(car_names)

    save_board(board.cars, saved_boards, board_hashes, car_names)
    
    complete = False
    n = 0
    s = 0
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

        board.move(random_car, random_move)

        comparison_result = compare_boards(board.cars, board_hashes, car_names)
        if comparison_result is not None:

            n = comparison_result
            create_board(board, size, n)

            boards_to_remove = saved_boards[n+1:] 
            for boardt in boards_to_remove:
                h = hash_board(boardt, car_names)
                board_hashes.pop(h, None)

            del saved_boards[n+1:]
            data.del_moves(n)

        else: 
            save_board(board.cars, saved_boards, board_hashes, car_names)
            n += 1

        s += 1
        complete = board.check_finish()
        if s%10000 == 0:
            print(f"loading, {s} steps")

    if complete:
        print(f"Puzzle solved in {n} moves!")
        board.data.export_moves()
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")