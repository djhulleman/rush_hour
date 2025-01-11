from data import *
import csv

class Board:
    '''create a board opject with the cars on it'''
    def __init__(self, filename, size, data):
        
        self.size = size
        self.data = data
        
        # create a self to store the cars in
        self.cars = {}
        
        # create a color range for the cars
        colors = [f"\033[38;5;{i}m" for i in [
            21,  # Bright blue
            34,  # Cyan
            46,  # Green
            50,  # Teal
            93,  # Magenta
            105, # Purple
            118, # Light green
            127, # Pink
            129, # Deep blue
            142, # Orange
            160, # Red-orange
            166, # Warm yellow
            172, # Bright yellow
            202, # Salmon
            208, # Coral
            220, # Golden yellow
            226, # Yellow
            231, # White
            10,  # Light Green
            12,  # Light Blue
            13,  # Light Magenta
            14,  # Light Cyan
            15,  # Light White
            16,  # Black
            17,  # Light Black
            18,  # Dark Grey
            19,  # Grey
            20,  # Light Grey
            22,  # Brown
            23,  # Dark Brown
            24,  # Olive Green
            25,  # Light Olive Green
            27,  # Pale Green
            28,  # Dark Teal
            30,  # Dark Purple
            32,  # Deep Blue
            35,  # Pink
            36,  # Dark Pink
            38,  # Deep Red
            39,  # Soft Red
            41,  # Dark Blue
            43,  # Teal Green
            45,  # Slate Blue
            47,  # Deep Aqua
            49   # Light Orange
        ]]
        
        
        # open and load game bord file
        with open(filename, mode ='r')as file:
            csvFile = csv.reader(file)
            # skip first line with information about the board
            next(csvFile)
            for i, lines in enumerate(csvFile):
                # store the car by using their names and add a color
                var_name = lines[0]
                # the X car is the car that needs to get out,
                # this car will be shown different (specific color)
                if lines[0] == 'X':
                    car = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), f"\033[38;5;1m")
                else:
                    car = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), colors[i])
                self.cars[var_name] = car


        # create matrix for board with all _
        self.board = [['_'] * size for _ in range(size)]
        # add the cars to the board
        for CAR in self.cars:
            car = self.cars[CAR]
            # see what the orientation is of the car and print it accordingly
            if car.orientation == "H":
                for j in range(0, car.length):
                    self.board[car.row-1][car.col+j-1] = car
            elif car.orientation == "V":
                for j in range(0, car.length):
                    self.board[car.row+j-1][car.col-1] = car

        self.history = []

    # print board
    def print(self):
        '''print current board'''
        for i in range(0, self.size):
            for j in range(0, self.size):
                car = self.board[i][j]
                if self.board[i][j] == '_':
                    print('_', end = '')
                else:
                    # car X; red car will be printed differently
                    if car.car =='X':
                        print(f"{car.color}{'X'}\033[0m", end ='')  
                    else:
                        print(f"{car.color}{'#'}\033[0m", end ='')
                print
                if j == self.size - 1:
                    print()
                else:
                    print(' ', end = '')
    
    def check_move(self, car, direction):
        '''check if the requested move is possible
        in game board'''
        # Get the car object
        car = self.cars[car]
        if car.orientation == "H":
            # Moving left
            if direction == 1:
                if car.col - 2 >= 0 and self.board[car.row - 1][car.col - 2] == '_':
                    return True
            # Moving right
            elif direction == 2:
                if car.col + car.length - 1 < self.size and self.board[car.row - 1][car.col + car.length - 1] == '_':
                    return True
        elif car.orientation == "V":
            # Moving up
            if direction == 1:
                if car.row - 2 >= 0 and self.board[car.row - 2][car.col - 1] == '_':
                    return True
                # Moving down
            elif direction == 2:
                if car.row + car.length - 1 < self.size and self.board[car.row + car.length - 1][car.col - 1] == '_':
                    return True
        return False
        
    def check_finish(board):
        '''check if red car is at the end'''
        XX = board.cars["X"] 
        # The "X" car is one step before the exit and the final position is empty
        if XX.col == board.size - 2 and board.board[XX.row - 1][board.size - 1] == '_':
            board.move('X',2)
            return True

    def move(self, car, direction):
        '''move car on game board'''
        # check if the car can move in the given direction
        if self.check_move(car, direction):
            car = self.cars[car]
            if car.orientation == "H":
                # the X car will be shown different
                if car.car == 'X':
                    # Moving left
                    if direction == 1:
                        self.board[car.row - 1][car.col - 2] = car
                        self.board[car.row - 1][car.col + car.length - 2] = '_'
                        # change position and save
                        car.col -= 1
                        self.data.save_move(car, direction)
                    # Moving right
                    if direction == 2:
                        self.board[car.row - 1][car.col - 1] = '_'
                        self.board[car.row - 1][car.col + car.length - 1] = car
                        car.col += 1
                        self.data.save_move(car, direction)
                else:
                    # Moving left
                    if direction == 1:
                        self.board[car.row - 1][car.col - 2] = car
                        self.board[car.row - 1][car.col + car.length - 2] = '_'
                        # change position and save
                        car.col -= 1
                        self.data.save_move(car, direction)
                    # Moving right
                    if direction == 2:
                        self.board[car.row - 1][car.col - 1] = '_'
                        self.board[car.row - 1][car.col + car.length - 1] = car
                        car.col += 1
                        self.data.save_move(car, direction)
            elif car.orientation == "V":
                # Moving up
                if direction == 1:
                    self.board[car.row - 2][car.col - 1] = car
                    self.board[car.row + car.length - 2][car.col - 1] = '_'
                    # change position and save
                    car.row -= 1
                    self.data.save_move(car, direction)
                # moving down
                if direction == 2:
                    self.board[car.row - 1][car.col - 1] = '_'
                    self.board[car.row + car.length - 1][car.col - 1] = car
                    car.row += 1
                    self.data.save_move(car, direction)
            else:
                print("FOUT") 
class Car:
    '''create a car object'''
    def __init__(self, car, orientation, col, row, length, color):
        self.car = car
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        self.color = color
