import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_move import *
from rushhour.algorithms.random_with_memory import *
from rushhour.algorithms.comparing import *
from rushhour.algorithms.BFS import breadth_first_search
from rushhour.algorithms.hillclimber import improve_solution
import time

"""
This script contains all functions for running the experiments per algorithm.
The script contains experiments for the algorithms:
1. random_move.py
2. random_with_memory.py
3. comparing.py
4. hillclimber.py
5. BFS.py
6. A*.py 
"""


def random_move_experiment(size, game, n):
    amount = []
    while len(amount) < n:
        # Create data process 
        data = Data()
        # create game board
        board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)
        
        steps = random_move(board)
        count = steps.data.count_moves()
        amount.append([count])
        
    new_file = f"baseline/stepcount_game{game}.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def random_with_memory_experiment(size, game, n):
    amount = []
    top_count = 0
    top = ''
    botom_count = 10000000000000
    botom = ''
    
    while len(amount) < n:
        memory = Memory()
        # Create data process 
        data = Data()
        # create game board
        board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)
        
        board_outcome = random_with_memory(board, memory)
        
        amount.append([board_outcome.count_moves()])
        if board_outcome.count_moves() > top_count:
            top_count = board_outcome.count_moves()
            top = board_outcome
        elif board_outcome.count_moves() < botom_count:
            botom_count = board_outcome.count_moves()
            botom = board_outcome
        
    top.export_moves(f"solutions/random_with_memory/top_game{game}.csv")
    botom.export_moves(f"solutions/random_with_memory/botom_game{game}.csv")
        
    new_file = f"solutions/random_with_memory/game{game}.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def compairing_experiment(board_file, size, game, n):
    amount = []
    count = 0
    top_count = 0
    top = ''
    botom_count = 10000000000000
    botom = ''
    while len(amount) < n:
        # run algorithem
        compare = Comparing(board_file, size)
        data = compare.run_comparing()
        steps = compare.get_steps()
        print(steps)
        count += 1
        print(f'round {count}')
        # store the steps
        amount.append([steps])
        if steps > top_count:
            top_count = steps
            top = data
        elif steps < botom_count:
            botom_count = steps
            botom = data
        
    top.export_moves(f"solutions/comparing_output/top_game{game}.csv")
    botom.export_moves(f"solutions/comparing_output/botom_game{game}.csv")
        
    new_file = f"solutions/comparing_output/game{game}.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def hillclimber_experiment():
    i = 0

    while True:

        board_best = improve_solution()

        board_best.data.export_moves(f'output{i}.csv')
        print("\n")

        i += 1

def BFS_experiment(size, game):

    data = Data()
    memory = Memory()
    board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

    start_time = time.time()

    breadth_first_search(board, memory)

    end_time = time.time()
    duration = end_time - start_time
 
    print(f'Algorithm took: {duration}')
        
        