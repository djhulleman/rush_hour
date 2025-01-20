from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.algorithms.random_with_memory import *
import csv
import random


size = 6
game = 1
board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"
 
def find_best_random(repetitions):
    i = 0
    n = float('inf')

    while i < repetitions:
        data = Data()
        memory = Memory()
        board = Board(f'{board_file}', size, data)

        board, t = random_with_memory(board, memory)
        if t < n:
            memory_best = memory
            board_best = board
            n = t
            print(f'New smallest number of steps: {n}')
        i += 1

    print(f'smalles number of steps {n}')

    return board_best, memory_best
            
def get_random_position(board_best, memory_best):
        length = len(board_best.data.output_data)
        car_names = board_best.cars.keys()
        
        random_pos = random.randint(0, length - 1)

        # delete saved hashes, boards and moves
        memory_best.del_hashes(memory_best, random_pos, car_names)
        del memory_best.saved_boards[random_pos+1:]
        board_best.data.del_moves(random_pos)     

board_best, memory_best = find_best_random(10)
board_best.data.export_moves('verbetermij.csv')

get_random_position(board_best, memory_best)
board_best.data.export_moves('cutted.csv')

random_with_memory(board_best, memory_best)
board_best.data.export_moves('output.csv')