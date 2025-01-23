from rushhour.classes.board import Board
from rushhour.classes.data import Data
from rushhour.classes.memory import Memory
from rushhour.algorithms.random_with_memory import random_with_memory
import random
import copy


size = 12
game = 7
board_file = f"../../gameboards/Rushhour{size}x{size}_{game}.csv"
solution_file = "output.csv"
 
def find_best_random(repetitions):
    i = 0
    n = float('inf')

    while i < repetitions:
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
        length = len(memory_best.saved_boards)
        car_names = board_best.cars.keys()
        
        random_pos = random.randint(0, length - 1)

        # delete saved hashes, boards and moves
        memory_best.del_hashes(memory_best, random_pos, car_names)
        del memory_best.saved_boards[random_pos+1:]
        board_best.data.del_moves(random_pos)

        # reset board object to random position
        memory_best.create_board(board_best, board_best.size, random_pos)

        return random_pos

from rushhour.classes.memory import *

def random_with_memory_for_hill(board, memory, random_pos, n_best):

    size = board.size
    car_names = board.cars.keys()
    car_list = list(car_names)

    # check if saved_boards is empty. This is necessary because random_with_memory.py is used in improve_solution.py
    if not memory.saved_boards:
        memory.save_board(board.cars, car_names)
        
    complete = False
    n = random_pos
    s = 0
    retry = 0
    reverse_index = random_pos
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

        board.move(random_car, random_move)

        comparison_result = memory.compare_boards(board.cars, car_names)
        if comparison_result is not None:

            reverse_index = max(comparison_result, random_pos)
            n = reverse_index

            memory.create_board(board, size, reverse_index)

            # delete saved hashes, boards and moves
            memory.del_hashes(memory, reverse_index, car_names)
            del memory.saved_boards[reverse_index+1:]
            board.data.del_moves(reverse_index)

        else: 
            memory.save_board(board.cars, car_names)
            n += 1

        if n > n_best - 1:
            n = random_pos
            reverse_index = random_pos

            memory.create_board(board, size, reverse_index)

            # delete saved hashes, boards and moves
            memory.del_hashes(memory, reverse_index, car_names)
            del memory.saved_boards[reverse_index+1:]
            board.data.del_moves(reverse_index)
            retry += 1
        
        if retry > 200:
            n = float('inf')
            print(f'no shorter solution found from cut')
            return board, n

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


def improve_solution():
     
    board_best, memory_best, n_best = find_best_random(1)
    board_best.data.export_moves('verbetermij.csv')

    while True:

        board = copy.deepcopy(board_best)
        memory = copy.deepcopy(memory_best)

        random_pos = get_random_position(board, memory)
        _, n = random_with_memory_for_hill(board, memory, random_pos, n_best)

        if n < n_best:
            n_best = n 
            board_best = board
            memory_best = memory
            
            print(f'shorter solution found, {n_best}')
            board_best.data.export_moves('output.csv')


if __name__ == "__main__":
     improve_solution()