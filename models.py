import numpy as np
import csv

class Board:
    '''create a board with the cars in it'''
    def __init__(self, filename, size):
        # create a color range for the cars
        colors = [f"\033[38;5;{i+4}m" for i in range(1, 256)]
        # create a self to store the cars in
        self.cars = []
        # open and load game bord file
        with open(filename, mode ='r')as file:
            csvFile = csv.reader(file)
            # skip first line with information about the board
            next(csvFile)
            for i, lines in enumerate(csvFile):
                # store the car by using there names and add a color
                var_name = lines[0]
                self.var_name = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), colors[i + 4])
                self.cars.append(self.var_name)

        
        # create matrix for board with all _
        self.board = [['_'] * size for _ in range(size)]
        # add the cars to the board
        for i in range(0, len(self.cars)):
            car = self.cars[i]
            # see what the orientation is of the car and print it accordingly
            if car.orientation == "H":
                for j in range(0, car.length):
                    self.board[car.row-1][car.col+j-1] = f"{car.color}{car.car}\033[0m"
            elif car.orientation == "V":
                for j in range(0, car.length):
                    self.board[car.row+j-1][car.col-1] = f"{car.color}{car.car}\033[0m"
    # print board
    def print(self):
        for row in self.board:
            print(' '.join(row))



class Car:
    '''create a car'''
    def __init__(self, car, orientation, col, row, length, color):
        self.car = car
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        self.color = color
