from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.classes.memory import Memory
from rushhour.algorithms.random_with_memory import random_with_memory
from datetime import datetime
import random
import copy
import time

solution_file = "output.csv"

def find_best_random(size, game, repetitions):
    """
    Function for finding a solution using the random_with_memory algorithm.
    Based on repetitions, function will run random_with_memory multiple times 
    and return the best solution
    """

    board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"

    i = 0 # counter for iterations
    n = float('inf') # set best solution as infinity 

    while i < repetitions:
        # initialize data, memory and board
        data_o = Data()
        memory = Memory()
        board = Board(f'{board_file}', size, data = data_o)

        board, t = random_with_memory(board, memory)
        if t < n:
            memory_best = copy.deepcopy(memory)
            board_best = copy.deepcopy(board)
            n = t
            print(f'New smallest number of steps: {n}')
        i += 1

    print(f'smalles number of steps {n}')

    return board_best, memory_best, n

            
def get_random_position(board_best, memory_best):
        """
        Function to get a random position withtin a given solution sequence
        """
        length = len(memory_best.saved_boards) # total saveed board states
        car_names = board_best.cars.keys() # list of car names
            
        # random slect a position within saved_boards
        random_pos = random.randint(0, length - 1)

        # delete saved hashes, boards and moves beyond the selected position
        memory_best.del_hashes(memory_best, random_pos, car_names)
        del memory_best.saved_boards[random_pos+1:]
        board_best.data.del_moves(random_pos)

        # reset board object to the selected random position
        memory_best.create_board(board_best, board_best.size, random_pos)

        return random_pos

from rushhour.classes.memory import *

def random_with_memory_for_hill(board, memory, random_pos, n_best):
    """
    Function to execute a random search like random_with_memory
    but adapted for the hillclimber function. 
    """

    size = board.size # board size
    car_names = board.cars.keys() # car names
    car_list = list(car_names) # list of car names

    # check if saved_boards is empty (initialize if necessary).
    if not memory.saved_boards:
        memory.save_board(board.cars, car_names)
        
    complete = False # used in loop condition
    n = random_pos # current position
    s = 0 # step counter
    retry = 0 # retry counter
    reverse_index = random_pos # reverse index
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        # select a random car and movement direction
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

        # try to move a car
        board.move(random_car, random_move)

        # compare the current board state with previously saved states
        comparison_result = memory.compare_boards(board.cars, car_names)
        if comparison_result is not None:
            
            # not a unique solution, reset board state to reverse_index. 
            # reverse_index cannot go beyond random_pos
            reverse_index = max(comparison_result, random_pos)
            n = reverse_index

            # recreate board state
            memory.create_board(board, size, reverse_index)

            # delete saved hashes, boards and moves
            memory.del_hashes(memory, reverse_index, car_names)
            del memory.saved_boards[reverse_index+1:]
            board.data.del_moves(reverse_index)

        else: 
            # its a unique solution, save board state
            memory.save_board(board.cars, car_names)
            n += 1


        # check if new solution is bigger than best solution
        if n > n_best - 1:
            # if bigger, reset to the starting position, random_pos
            n = random_pos
            reverse_index = random_pos

            # recreate board state at random_pos
            memory.create_board(board, size, reverse_index)

            # delete saved hashes, boards and moves
            memory.del_hashes(memory, reverse_index, car_names)
            del memory.saved_boards[reverse_index+1:]
            board.data.del_moves(reverse_index)

            # count as unseccesfull
            retry += 1 
        
        # stop if too many tries were unseccesfull 
        if retry > 200:
            n = float('inf')
            #print(f'no shorter solution found from cut')
            return False, float('inf')

        s += 1
        complete = board.check_finish()
        # if s%50000 == 0:
        #     print(f"loading, {s} steps")

    if complete:
        n += 1 # Last step is made inside board.check_finish()
        #print(f"Puzzle solved in {n} moves!")
        return board, n
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")


def hillclimber(size, game):
    """
    Function to improve a solution iteratively
    """
    
    # get initial board from random_with_memory algorithm
    board_best, memory_best, n_best = find_best_random(size, game, 1)
    board_best.data.export_moves('verbetermij.csv')

    max_no_solution = 100
    no_solution = 0
    start_time_seconds = time.time()
    run_time = 0

    # loop until the runtime exceeds limit
    while run_time < 5400:

        # copy best board and memory states
        board = copy.deepcopy(board_best)
        memory = copy.deepcopy(memory_best)

        # get a random position and attempt to improve the solution
        random_pos = get_random_position(board, memory)
        board, n = random_with_memory_for_hill(board, memory, random_pos, n_best)

        if board == False:
            no_solution += 1
        else: 
            no_solution = 0

        # check if a shorter solution is found
        if n < n_best:

            # save board as new best solution
            n_best = n 
            board_best = board
            memory_best = memory

            # track progress, time and export data
            current_time= datetime.now()
            current_time_seconds = time.time()
            run_time = current_time_seconds - start_time_seconds
            
            print(f'shorter solution found, {n_best}:   ', current_time.strftime("%H:%M:%S"), run_time)
            board_best.data.export_moves('output.csv')

        # track time
        current_time_seconds =  time.time()
        run_time = current_time_seconds - start_time_seconds

    return board_best


if __name__ == "__main__":

    i = 0
    size = 9
    game = 5

    while True:

        board_best = hillclimber(size, game)

        board_best.data.export_moves(f'output{i}.csv')
        print("\n")

        i += 1