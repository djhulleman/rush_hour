import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_move import *
from rushhour.algorithms.random_with_memory import *
from rushhour.algorithms.comparing import *
from rushhour.algorithms.BFS import breadth_first_search
from rushhour.algorithms.hillclimber import hillclimber
from rushhour.algorithms.Astar import A_Star
import time
import os

"""
This script contains functions for running experiments per algorithm.
The script contains experiments for the following algorithms:
1. random_move.py
2. random_with_memory.py
3. comparing.py
4. hillclimber.py
5. BFS.py
6. A*.py 
"""


def random_move_experiment(size, game, n):
    """
    Runs the random_move algorithm n times for the specified board size and game.
    - exports the step count data for each run to the "baseline" folder
    """
    amount = []
    while len(amount) < n:
        # create data process 
        data = Data()
        # create game board
        board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)
        
        # run random_move algorithm
        steps = random_move(board)
        count = steps.data.count_moves()
        amount.append([count])
        
    # export step count data to a csv
    new_file = f"baseline/stepcount_game{game}.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def random_with_memory_experiment(size, game, n):
    """
    Runs the random_with_memory algorithm n times for the specified board size and game.
    - exports the best and worst solution to "solutions/random_with_memory"
    - exports the step count data for all runds to a csv file.
    """
    amount = []
    top_count = 0
    top = ''
    botom_count = 10000000000000 # change to float('inf')?
    botom = ''
    
    while len(amount) < n:
        memory = Memory()
        # Create data process 
        data = Data()
        # create game board
        board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)
        
        # run the random_with_memory algorithm
        board_outcome = random_with_memory(board, memory)
        
        # determine best and worst solutions
        amount.append([board_outcome.count_moves()])
        if board_outcome.count_moves() > top_count:
            top_count = board_outcome.count_moves()
            top = board_outcome
        elif board_outcome.count_moves() < botom_count:
            botom_count = board_outcome.count_moves()
            botom = board_outcome
        
    # export best and worst solutions
    top.export_moves(f"solutions/random_with_memory/top_game{game}.csv")
    botom.export_moves(f"solutions/random_with_memory/botom_game{game}.csv")
        
    # export step count data to csv file
    new_file = f"solutions/random_with_memory/game{game}.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def compairing_experiment(board_file, size, game, n):
    """
    Runs the comparing algorithm n times and tracks the performace.
    - exports the best and worst solutions to "solutions/comparing_output".
    - exports step count data for all runs to a csv fole.
    """
    amount = []
    count = 0
    top_count = 0
    top = ''
    botom_count = 10000000000000
    botom = ''
    while len(amount) < n:
        # run comparing algorithm
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
        
    # export the best and worst solution
    top.export_moves(f"solutions/comparing_output/top_game{game}.csv")
    botom.export_moves(f"solutions/comparing_output/botom_game{game}.csv")
        
    # export step count data to csv.
    new_file = f"solutions/comparing_output/game{game}.csv"  
    with open(new_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(amount)

def hillclimber_experiment(size, game):
    """
    Continuesly runs the hillclimber algorithm for a given period.
    - solution and their time are printed in the terminal
    - each cycle the best solution is exported to a file "output{i}.csv"
    """
    i = 0                       # counts each time a new hillclimber cycle is started
    run_time = 0                # initialize run_time variable 
    start_time = time.time()    # save start time of algorithm
    max_runtime = 36000        # 36000 seconds = 10 hour

    while run_time < max_runtime :
        # run  hillclimber algorithm
        board_best = hillclimber(size, game)

        # export best solution to csv file
        board_best.data.export_moves(f'solutions/Hillclimber/output{i}.csv')
        print("\n")

        i += 1

        # calculate run time
        current_time = time.time()
        run_time = current_time - start_time

    # delete unneseccary files when conducting experiment
    file_path1 = "solutions/Hillclimber/output.csv"
    file_path2 = "solutions/Hillclimber/original_solution.csv"

    if os.path.exists(file_path1):
        os.remove(file_path1)
    if os.path.exists(file_path2):
        os.remove(file_path2)


def BFS_experiment(size, game):
    """
    Runs the Breath-First-Search (BFS.py) algrithm and measures the run time.
    - exports the best solution 
    - prints the time taken to find the best solution
    """

    data = Data()
    memory = Memory()
    board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

    start_time = time.time()

    breadth_first_search(board, memory)

    end_time = time.time()
    duration = end_time - start_time
 
    print(f'Algorithm took: {duration}')

def A_Star_experiment(size, game):
    """
    Runs the A* algorithm and measures the run time
    - exports the best solution
    - prints the time taken to find the best solution
    """

    data = Data()
    board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

    start_time = time.time()

    A_Star(board)

    end_time = time.time()
    duration = end_time - start_time
 
    print(f'Algorithm took: {duration}')