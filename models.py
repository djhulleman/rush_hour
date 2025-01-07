import numpy as np
import csv

class Board:


    def __init__(self, filename, size):
        colors = [f"\033[38;5;{i+4}m" for i in range(1, 256)]

        self.cars = []
        with open(filename, mode ='r')as file:
            csvFile = csv.reader(file)
            next(csvFile)
            for i, lines in enumerate(csvFile):
                var_name = lines[0]
                self.var_name = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]), colors[i + 4])
                self.cars.append(self.var_name)

        self.board = [['_'] * size for _ in range(size)]
        for i in range(0, len(self.cars)):
            car = self.cars[i]
            if car.orientation == "H":
                for j in range(0, car.length):
                    self.board[car.row-1][car.col+j-1] = f"{car.color}{car.car}\033[0m"
        
        for i in range(0, len(self.cars)):
            car = self.cars[i]
            if car.orientation == "V":
                for j in range(0, car.length):
                    self.board[car.row+j-1][car.col-1] = f"{car.color}{car.car}\033[0m"

    def print(self):
        for row in self.board:
            print(' '.join(row))



class Car:
    def __init__(self, car, orientation, col, row, length, color):
        self.car = car
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        self.color = color
