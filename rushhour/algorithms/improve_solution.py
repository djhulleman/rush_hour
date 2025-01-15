from rushhour.classes.board import Board
from rushhour.classes.car import Car
from rushhour.classes.data import Data
from rushhour.algorithms.random_with_memory import *
import csv
import random

output_file = '../../output.csv'
size = 6
game = 1
file_name = f'../../gameboards/Rushhour{size}x{size}_{game}.csv'
data = Data()

board = Board(file_name, size, data)

def random_position(output_file):

    with open(output_file, mode='r') as file:
        csvFile = list(csv.reader(file))

        csv_rows = csvFile[1:]
        csv_length = len(csv_rows)
        print(csv_rows)
        print(csv_length)

        random_position = random.randint(0, csv_length - 1)
        del csv_rows[random_position:]

        for i, lines in enumerate(csv_rows):
            direction = 0
            move = int(lines[1]) 
            if move == 1:
                direction = 2
            elif move == -1:
                direction = 1
            board.move(lines[0], direction)
            i
            if i == random_position:
                break
        return csv_rows 

csv_rows = random_position(output_file)
random_with_memory(csv_rows)
board.print()

