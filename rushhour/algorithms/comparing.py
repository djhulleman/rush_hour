from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_with_memory import *
from rushhour.classes.memory import *
from itertools import combinations
from copy import deepcopy
import random

class Comparing:
    '''compares random paths with one another to find a overlaping path.
    than follow said path to try and find a batter path'''
    
    def __init__(self, board_file, size):
        self.file = board_file
        self.size_game = size
        # make empty dict
        self.paths = {}
        self.overlap_results = {}
        self.best_path = {}
        self.best = 0
    
    def solve_with_memory(self, board, bool, data = None):
        '''solves a game using random staps'''
        memory = Memory()
        size = board.size
        car_names = board.cars.keys()
        car_list = list(car_names)
        # save board in memory
        memory.save_board(board.cars, car_names)
            
        complete = False
        n = 0
        # Prevent infinite loops
        max_iterations = 10000000
        i = 1
        # when data is given, follow these steps untill empty
        while bool is True:
            # while data are not done
            if i < len(data):
                car = data[i][0]
                move = data[i][1]
                # change steps to steps that can be read by move function
                if move == '1':
                    move = 2
                else:
                    move = 1
                i += 1
                # is stap is possible
                if board.check_move(car, move):
                    # take the step
                    board.move(car, move)
                    # store board in memory
                    comparison_result = memory.compare_boards(board.cars, car_names)
                    memory.save_board(board.cars, car_names)
                    n += 1
                    complete = board.check_finish()
            else:
                bool = False
                break
        # is no data is provided or data is empty
        while not complete and n < max_iterations:
            # make random car and move
            random_car = random.choice(car_list)
            random_move = random.choice([1, 2])
            # see if move is valid
            if board.check_move(random_car, random_move):
                # move car
                board.move(random_car, random_move)
                # compar board with privious board to see is overlap is pressent
                comparison_result = memory.compare_boards(board.cars, car_names)
                # if overlap is pressent
                if comparison_result is not None:
                    # deleate overlap
                    n = comparison_result
                    memory.create_board(board, size, n)
                    # delete saved hashes, boards and moves
                    memory.del_hashes(memory, n, car_names)
                    del memory.saved_boards[n+1:]
                    board.data.del_moves(n)
                # if overlap is not pressent
                else: 
                    # save board
                    memory.save_board(board.cars, car_names)
                # see if car is at the end
                complete = board.check_finish()

            if complete:
                # return the stap data
                memory.saved_boards.clear()
                memory.board_hashes.clear()
                return board.data
            
    def compare_files(self, path1, path2):
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
            
    def make_first_pool(self, n):
        '''take random paths'''
        teller = 0
        # find 50 paths
        while teller < n:
            # make a board
            board = Board(self.file, self.size_game)
            # make rendomly a path
            steps = self.solve_with_memory(board, False)
            # store path and steps
            self.paths[steps] = steps.count_moves()
            teller += 1

    def get_highest_compar(self, n):
        '''compair random paths'''
        # sort the dict
        sorted_items = sorted(self.paths.items(), key=lambda item: item[1])
        # Get the top smallest items
        top_list = sorted_items[:n]
        # Compare all pairs of the top items
        for path1, path2 in combinations(top_list, 2):
            list_overlap = self.compare_files(path1[0].output_data, path2[0].output_data)
            # store path and steps
            self.overlap_results[list_overlap] = list_overlap.count_moves()
        self.paths.clear()

    def make_second_pool(self, overlap_data, n):
        '''do random n times and save path'''
        N = 0
        while N < n:
            data = deepcopy(overlap_data)
            # make board
            board_overlap = Board(self.file, self.size_game)
            # using the overlapping steps first, make a new path
            steps = self.solve_with_memory(board_overlap, True, data.output_data)
            # store path and steps
            self.best_path[steps] = steps.count_moves()
            N += 1
        
    def run_comparing(self):
        '''algarithem that finds the best path'''
        # make 50 paths
        self.make_first_pool(20)
        print("one done")
        # compair the paths and make a top 30
        self.get_highest_compar(14)
        print("two done")
        # Get the maximum overlap result
        # get the steps amount
        max_overlap = max(self.overlap_results.values())
        # get the joint dataset
        max_key = next(pair for pair, overlap in self.overlap_results.items() if overlap == max_overlap)
        print(max_key.output_data)
        # make 20 new paths
        self.make_second_pool(max_key, 8)
        '''take the fastes path and make it the output'''
        # find the fastest path
        # get the steps
        self.best = min(self.best_path.values())
        # get the joined data
        path = next(pair for pair, overlap in self.best_path.items() if overlap == self.best)
        # return the data of the best path
        return path
    
    def get_steps(self):
        '''returns the amount of steps made'''
        return self.best
