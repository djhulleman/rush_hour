import random

class Memory:
    def __init__(self):
        self.saved_boards = []
        self.board_hashes = {}

    def hash_board(self, board_copy, car_names):
        cars_properties = []
        for key in car_names:
            r, c = board_copy[key]
            cars_properties.append(f"{key}:{r}:{c}")
        return "|".join(cars_properties)
        
    def save_board(self, cars, car_names):
        board_copy = {}
        for key, car in cars.items():
            board_copy[key] = (car.row, car.col)
        
        self.saved_boards.append(board_copy)

        h = self.hash_board(board_copy, car_names)
        self.board_hashes[h] = len(self.saved_boards) - 1

    def compare_boards(self, cars, car_names):
        current_board_copy = {}
        for key, car in cars.items():
            current_board_copy[key] = (car.row, car.col)

        h = self.hash_board(current_board_copy, car_names)
        return self.board_hashes.get(h, None)

    def create_board(self, board, size, position):

        board.board = [['_'] * size for _ in range(size)]

        # Get car properties from saved_boards list 
        saved_board = self.saved_boards[position]

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