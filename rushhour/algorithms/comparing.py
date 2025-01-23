from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_with_memory import *
from rushhour.classes.memory import *
from itertools import combinations
from copy import deepcopy


def make_dict(steps, dict): 
    '''make dict using the size and the steps'''
    # Count the lines in the file to store it with the file name
    line_count = len(steps.output_data)
    dict[steps] = line_count
        
def compare_files(path1, path2):
    '''see how much file compair and save the comapires'''
    # make new empty data object
    data = Data()
    memory = Memory
    i = 1
    j = 1
    # Find the overlap
    while i < len(path1) and j < len(path2):
        if path1[i] == path2[j]:
            # store the moves in the data
            data.save_list_moves(path1[i][0], path1[1][1])
            i += 1
            j += 1
        else:
            break
    # return the data
    return data

def get_memory(board):
    data = board.data.output_data
    memory = Memory()
    car_names = board.cars.keys()
    memory.save_board(board.cars, car_names)
    i = 1
    while i< len(data):
        board.move(data[i][0], data[1][1])
        memory.save_board(board.cars, car_names)
        i += 1
    return memory, i
    
def run_comparing(board_file, size):
    '''algarithem that finds the best path'''
    
    '''take random paths'''
    # make empty dict
    paths = {}
    combined = {}
    teller = 0
    # find 20 paths
    while teller < 10:
        memory_begin = Memory()
        # make a board
        board = Board(board_file, size)
        # make rendomly a path
        steps, amount = random_with_memory(board, memory_begin)
        make_dict(steps, paths)
        teller += 1
    '''compair rendom paths'''
    # sort the dict
    sorted_items = sorted(paths.items(), key=lambda item: item[1])
    # Get the top 10 smallest items
    top_10 = sorted_items[:10]
    # make a new dict
    overlap_results = {}
    # Compare all pairs of the top 10 items
    for path1, path2 in combinations(top_10, 2):
        list_overlap = compare_files(path1[0].output_data, path2[0].output_data)
        # make a dict
        make_dict(list_overlap, overlap_results)
    # Get the maximum overlap result
    max_overlap = max(overlap_results.values())
    max_key = next(pair for pair, overlap in overlap_results.items() if overlap == max_overlap)
    print(max_key.output_data)
    

    '''do random n times and save path'''
    N = 0
    # make an empty dict
    best_path = {}
    while N < 10:
        memory = Memory()
        data = deepcopy(max_key)
        # use the data with overlapping staps and make a board
        board_overlap = Board(board_file, size, data)
        memory, items = get_memory(board_overlap)
        steps, amount = random_with_memory(board_overlap, memory, items)
        # make a dict
        make_dict(steps, best_path)
        N += 1
    '''take the fastes path and make it the output'''
    # find the fastest path
    best = min(best_path.values())
    path = next(pair for pair, overlap in best_path.items() if overlap == best)
    # save the output of the best path
    new_file = "solutions/compair_path.csv"
    path.export_moves(new_file)
    return best