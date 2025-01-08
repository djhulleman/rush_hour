import numpy as np
import csv

class Board:
    '''create a board with the cars in it'''
    def __init__(self, filename, size):
        # create a color range for the cars
        colors = [f"\033[38;5;{i+4}m" for i in range(1, 256)]
        # create a self to store the cars in
        self.size = size
        self.cars = {}
        # open and load game bord file
        with open(filename, mode ='r')as file:
            csvFile = csv.reader(file)
            # skip first line with information about the board
            next(csvFile)
            for i, lines in enumerate(csvFile):
                # store the car by using their names and add a color
                var_name = lines[0]
                if lines[0] == 'X':
                    car = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), colors[4])
                else:
                    car = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), colors[i + 5])
                self.cars[var_name] = car

        # create matrix for board with all _
        self.board = [['_'] * size for _ in range(size)]
        # add the cars to the board
        for CAR in self.cars:
            car = self.cars[CAR]
            # see what the orientation is of the car and print it accordingly
            if car.orientation == "H":
                for j in range(0, car.length):
                    self.board[car.row-1][car.col+j-1] = f"{car.color}{'#'}\033[0m"
            elif car.orientation == "V":
                for j in range(0, car.length):
                    self.board[car.row+j-1][car.col-1] = f"{car.color}{'#'}\033[0m"
    # print board
    def print(self):
        for row in self.board:
            print(' '.join(row))
    
    def check_move(self, car, direction):
        car = self.cars[car]  # Get the car object
        if car.orientation == "H":
            if direction == 1:  # Moving left
                if car.col - 2 >= 0 and self.board[car.row - 1][car.col - 2] == '_':
                    return True
            elif direction == 2:  # Moving right
                if car.col + car.length - 1 < self.size and self.board[car.row - 1][car.col + car.length - 1] == '_':
                    return True
        elif car.orientation == "V":
            if direction == 1:  # Moving up
                if car.row - 2 >= 0 and self.board[car.row - 2][car.col - 1] == '_':
                    return True
            elif direction == 2:  # Moving down
                if car.row + car.length - 1 < self.size and self.board[car.row + car.length - 1][car.col - 1] == '_':
                    return True
        return False


    def move(self, car, direction):
        if self.check_move(car, direction):
            car = self.cars[car]
            if car.orientation == "H":
                if direction == 1:
                    self.board[car.row - 1][car.col - 2] = f"{car.color}{'#'}\033[0m"
                    self.board[car.row - 1][car.col + car.length - 2] = '_'
                    car.col -= 1
                if direction == 2:
                    self.board[car.row - 1][car.col - 1] = '_'
                    self.board[car.row - 1][car.col + car.length - 1] = f"{car.color}{'#'}\033[0m"
                    car.col += 1
            elif car.orientation == "V":
                if direction == 1:
                    self.board[car.row - 2][car.col - 1] = f"{car.color}{'#'}\033[0m"
                    self.board[car.row + car.length - 2][car.col - 1] = '_'
                    car.row -= 1
                if direction == 2:
                    self.board[car.row - 1][car.col - 1] = '_'
                    self.board[car.row + car.length - 1][car.col - 1] = f"{car.color}{'#'}\033[0m"
                    car.row += 1
            else:
                print("FOUT") 
class Car:
    '''create a car'''
    def __init__(self, car, orientation, col, row, length, color):
        self.car = car
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        self.color = color
