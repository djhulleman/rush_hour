import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_with_memory import *
from rushhour.classes.memory import *
from itertools import combinations
import time
import os

def run_compairing(size, game):

    # Create data process 
    board_file = f'gameboards/Rushhour{size}x{size}_{game}.csv'


    # Helper function to create a unique file name based on timestamp
    def generate_unique_filename():
        # Current timestamp in nanoseconds
        timestamp = time.time_ns()
        return f"output_{timestamp}.csv"

    def make_dict(steps, dict): 
        # Count the lines in the file to store it with the file name
        line_count = len(steps.output_data)  # count lines in file
        dict[steps] = line_count
            

    def compare_files(path1, path2):
        '''see how much file compair and save the comapires'''
        data = Data()
        i = 1
        j = 1
        # Find the overlap
        while i < len(path1) and j < len(path2):
            if path1[i] == path2[j]:
                data.save_list_moves(path1[i][0], path1[1][1])
                i += 1
                j += 1
            else:
                break 
        return data
    

    '''take random paths'''
    paths = {}
    teller = 0
    while teller < 20:
        data = Data()
        memory_begin = Memory()
        board = Board(board_file, size, data)
        # make rendomly a path
        finished = random_with_memory(board, memory_begin)
        # save the steps
        steps = finished.data
        make_dict(steps, paths)
        teller += 1

    '''compair rendom paths'''
    sorted_items = sorted(paths.items(), key=lambda item: item[1])
    # Get the top 10 smallest items
    top_10 = sorted_items[:10]
    overlap_results = {}
    # Compare all pairs of the top 10 items
    for path1, path2 in combinations(top_10, 2):
        list_overlap = compare_files(path1[0].output_data, path2[0].output_data)
        make_dict(list_overlap, overlap_results)
    # Get the maximum overlap result
    max_overlap = max(overlap_results.values())
    max_key = next(pair for pair, overlap in overlap_results.items() if overlap == max_overlap)

    '''do random n times and save path'''
    N = 0
    best_path = {}
    while N < 10:
        # genereer een bord met de overlap stappen,
        # sla daarna de rendom stappen erbij op
        memory_new_path = Memory()
        board_overlap = Board(board_file, size, max_key)
        finished = random_with_memory(board_overlap, memory_new_path)
        # save the steps
        steps = finished.data
        make_dict(steps, best_path)
        N += 1

    '''take the fastes path and make it the output'''
    best = min(best_path.values())
    path = next(pair for pair, overlap in best_path.items() if overlap == best)
    new_file = "solutions/compair_path.csv"
    path.export_moves(new_file)
