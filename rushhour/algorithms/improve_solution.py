from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.algorithms.random_with_memory import *
import csv
import random

size = 6
game = 1
board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"
# Create data processes
data = Data()
memory = Memory()
# create game board
board = Board(f'{board_file}', size, data)

n = random_with_memory(board, memory)

def find_best_path(board, input_csv):
    print()
    


def random_position(input_csv):

    with open(input_csv, mode='r') as input_file, open('cutted_csv.csv', mode='w', newline='') as output_file:
        # Get length of csv file
        csvFile_list = list(csv.reader(input_file))
        csv_length = len(csvFile_list)
        random_pos = random.randint(1, csv_length - 1)

        input_file.seek(0)

        csv_inputFile = csv.reader(input_file)
        csv_outputFile = csv.writer(output_file)

        for i, lines in enumerate(csv_inputFile):
            csv_outputFile.writerow(lines)
            if i == random_pos:
                break

def set_board(board):

    with open('cutted_csv.csv', mode='r', newline='') as file:
        cutted_csv = csv.reader(file)
        next(cutted_csv, None)
        
        for lines in cutted_csv:
            direction = 0
            move = int(lines[1]) 
            if move == 1:
                direction = 2
            elif move == -1:
                direction = 1
            board.move(lines[0], direction)
            #save_board(board.cars, board.cars.keys())