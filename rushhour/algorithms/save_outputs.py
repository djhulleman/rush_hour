from game import *
import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_move import *
from rushhour.algorithms.random_with_memory import *
from rushhour.algorithms.comparing import *


def randomly_save(size, game, n):
    amount = []
    while len(amount) < n:
        # Create data process 
        data = Data()
        # create game board
        board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)
        
        steps = random_solve(board)
        amount.append([steps])
        
    new_file = "rendom_output_test.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def random_memory_save(size, game, n):
    amount = []
    while len(amount) < n:
        memory = Memory()
        # Create data process 
        data = Data()
        # create game board
        board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)
        
        baord, steps = random_with_memory(board, memory)
        amount.append([steps])
        
    new_file = "rendom_with_memory_output_test.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def compairing_save(size, game, n):
    amount = []
    while len(amount) < n:
        steps = run_comparing(size, game)
        amount.append([steps])
        
    new_file = "comparing_output_test.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)