from rushhour.classes.board import Board
from rushhour.classes.car import Car
from rushhour.classes.data import Data
import csv

output_file = 'output.csv'
size = 6
game = 1
file_name = f'gameboards/Rushhour{size}x{size}_{game}.csv'
data = Data()

board = Board(file_name, size, data)

with open(output_file, mode='r') as file:
    csvFile = csv.reader(file)
    next(csvFile)
    for i, lines in enumerate(csvFile):
        direction = 0
        move = int(lines[1])  # Convert the value to an integer
        if move == 1:
            direction = 2
        elif move == -1:
            direction = 1
        board.move(lines[0], direction)

        print(f"{lines[0]}", move, direction)

board.print()
