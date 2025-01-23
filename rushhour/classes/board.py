import csv
from rushhour.classes.car import Car
from rushhour.classes.data import Data
from rushhour.classes.memory import Memory


class Board:
    '''create a board opject with the cars on it'''
    def __init__(self, filename, size, data = None):
        if data == None:
            data = Data()
        self.size = size
        self.data = data
        self.name = filename
        
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
        
    def check_finish(board):
        '''check if red car is at the end'''
        XX = board.cars["X"] 
        # The "X" car is one step before the exit and the final position is empty
        if XX.col == board.size - 2 and board.board[XX.row - 1][board.size - 1] == '_':
            board.move('X',2)
            return True

    def check_move(self, car, direction, steps=1):
        '''check if the requested move is possible
        in game board for multiple steps'''
        # Get the car object
        car = self.cars[car]

        if car.orientation == "H":  # Horizontal movement
            if direction == 1:  # Moving left
                if car.col - 2 - (steps - 1) >= 0:  # Ensure there’s enough space to move
                    # Check all cells along the left path for empty spaces
                    return all(self.board[car.row - 1][car.col - 2 - i] == '_' for i in range(steps))
            elif direction == 2:  # Moving right
                if car.col + car.length - 1 + (steps - 1) < self.size:  # Ensure there’s enough space to move
                    # Check all cells along the right path for empty spaces
                    return all(self.board[car.row - 1][car.col + car.length - 1 + i] == '_' for i in range(steps))

        elif car.orientation == "V":  # Vertical movement
            if direction == 1:  # Moving up
                if car.row - 2 - (steps - 1) >= 0:  # Ensure there’s enough space to move
                    # Check all cells along the upward path for empty spaces
                    return all(self.board[car.row - 2 - i][car.col - 1] == '_' for i in range(steps))
            elif direction == 2:  # Moving down
                if car.row + car.length - 1 + (steps - 1) < self.size:  # Ensure there’s enough space to move
                    # Check all cells along the downward path for empty spaces
                    return all(self.board[car.row + car.length - 1 + i][car.col - 1] == '_' for i in range(steps))

        # If none of the conditions are satisfied, the move is not possible
        return False

        
    def move(self, car, direction, steps=1):
        '''move car on game board'''
        if not self.check_move(car, direction, steps):  # Pass car's name to check_move
            print("Invalid move")
            return

        car = self.cars[car]  # Access the Car object after validation

        if car.orientation == "H":
            for _ in range(steps):  # Move the car step by step
                if car.car == 'X':
                    if direction == 1:  # Moving left
                        self.board[car.row - 1][car.col - 2] = car
                        self.board[car.row - 1][car.col + car.length - 2] = '_'
                        car.col -= 1
                    elif direction == 2:  # Moving right
                        self.board[car.row - 1][car.col - 1] = '_'
                        self.board[car.row - 1][car.col + car.length - 1] = car
                        car.col += 1
                else:
                    if direction == 1:  # Moving left
                        self.board[car.row - 1][car.col - 2] = car
                        self.board[car.row - 1][car.col + car.length - 2] = '_'
                        car.col -= 1
                    elif direction == 2:  # Moving right
                        self.board[car.row - 1][car.col - 1] = '_'
                        self.board[car.row - 1][car.col + car.length - 1] = car
                        car.col += 1

        elif car.orientation == "V":
            for _ in range(steps):  # Move the car step by step
                if direction == 1:  # Moving up
                    self.board[car.row - 2][car.col - 1] = car
                    self.board[car.row + car.length - 2][car.col - 1] = '_'
                    car.row -= 1
                elif direction == 2:  # Moving down
                    self.board[car.row - 1][car.col - 1] = '_'
                    self.board[car.row + car.length - 1][car.col - 1] = car
                    car.row += 1

        # Save the move as a single action
        self.data.save_move(car, direction, steps)
                