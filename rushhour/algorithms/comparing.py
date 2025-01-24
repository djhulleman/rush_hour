from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_with_memory import *
from rushhour.classes.memory import *
from itertools import combinations
from copy import deepcopy
import random


def solve_with_memory(board, bool, data = None):
    memory = Memory()
    size = board.size
    car_names = board.cars.keys()
    car_list = list(car_names)

    memory.save_board(board.cars, car_names)
        
    complete = False
    n = 0
    max_iterations = 10000000  # Prevent infinite loops
    i = 1
    while bool == True:
        if i < len(data):
            car = data[i][0]
            move = data[i][1]
            if move == '1':
                move = 2
            else:
                move = 1
            if board.check_move(car, move):
                board.move(car, move)
                comparison_result = memory.compare_boards(board.cars, car_names)
                memory.save_board(board.cars, car_names)
                i += 1
                n += 1
                complete = board.check_finish()
            else:
                bool = False

    while not complete and n < max_iterations:
        
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])
        if board.check_move(random_car, random_move):
            board.move(random_car, random_move)
        
            comparison_result = memory.compare_boards(board.cars, car_names)
            if comparison_result is not None:

                n = comparison_result
                memory.create_board(board, size, n)

                # delete saved hashes, boards and moves
                memory.del_hashes(memory, n, car_names)
                del memory.saved_boards[n+1:]
                board.data.del_moves(n)

            else: 
                memory.save_board(board.cars, car_names)
            complete = board.check_finish()

        if complete:
            return board.data




def make_dict(steps, dict, line_count): 
    '''make dict using the size and the steps'''
    # Count the lines in the file to store it with the file name
    dict[steps] = line_count
        
def compare_files(path1, path2):
    '''see how much file compair and save the comapires'''
    # make new empty data object
    data = Data()
    i = 1
    # Find the overlap
    while i < len(path1) and i < len(path2):
        if path1[i] == path2[i]:
            # store the moves in the data
            data.save_list_moves(path1[i][0], path1[i][1])
            i += 1
        else:
            # return the data
            return data


    
def run_comparing(board_file, size):
    '''algarithem that finds the best path'''
    
    '''take random paths'''
    # make empty dict
    paths = {}
    teller = 0
    # find 20 paths
    while teller < 50:
        # make a board
        board = Board(board_file, size)
        # make rendomly a path
        steps = solve_with_memory(board, False)
        make_dict(steps, paths, steps.count_moves())
        teller += 1
    '''compair rendom paths'''
    # sort the dict
    sorted_items = sorted(paths.items(), key=lambda item: item[1])
    # Get the top smallest items
    top_list = sorted_items[:30]
    # make a new dict
    overlap_results = {}
    # Compare all pairs of the top 10 items
    for path1, path2 in combinations(top_list, 2):
        list_overlap = compare_files(path1[0].output_data, path2[0].output_data)
        # make a dict
        make_dict(list_overlap, overlap_results, list_overlap.count_moves())
    # Get the maximum overlap result
    max_overlap = max(overlap_results.values())
    max_key = next(pair for pair, overlap in overlap_results.items() if overlap == max_overlap)
    print(max_key.output_data)
    

    '''do random n times and save path'''
    N = 0
    # make an empty dict
    best_path = {}
    while N < 20:
        data = deepcopy(max_key)
        # use the data with overlapping staps and make a board
        board_overlap = Board(board_file, size)
        steps = solve_with_memory(board_overlap, True, data.output_data)
        # make a dict
        make_dict(steps, best_path, steps.count_moves())
        N += 1
    '''take the fastes path and make it the output'''
    # find the fastest path
    best = min(best_path.values())
    path = next(pair for pair, overlap in best_path.items() if overlap == best)
    # save the output of the best path
    # new_file = "solutions/compair_path.csv"
    new_file = "output.csv"
    path.export_moves(new_file)
    return best
