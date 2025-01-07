import numpy as np
from models import *
import csv

def get_cars(filename):
    cars = []
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        next(csvFile)
        for lines in csvFile:
            var_name = lines[0]  # Use the first element as the variable name
            globals()[var_name] = Car(lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4]))
            cars.append(globals()[var_name])
    return cars

def create_board(n):
    board = np.full((n, n), '_', dtype=str)
    return board

def place_cars(board, cars):
    for i in range(0, len(cars)):
        car = cars[i]
        if car.orientation == "H":
            for j in range(0, car.length):
                board[car.row-1][car.col+j-1] = car.car
    
    for i in range(0, len(cars)):
        car = cars[i]
        if car.orientation == "V":
            for j in range(0, car.length):
                board[car.row+j-1][car.col-1] = car.car
    return board