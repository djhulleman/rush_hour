from collections import deque
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.shorten_csv import combine_moves
import csv

def bfs_solver(board, memory):
    """
    Perform a BFS to find the shortest solution path 
    """
    # save the initial state in memory and save its index
    car_names = board.cars.keys()
    memory.save_board(board.cars, car_names)
    start_index = len(memory.saved_boards) - 1

    # use a queue of indexes linked to memory.saved_boards 
    queue = deque([start_index])

    # keep track of paths:  paths[state_index] = list of moves from start
    paths = {start_index: []}

    # perform bfs till queue is empty 
    while queue:
        # get the first index in queue
        current_index = queue.popleft()
        
        # rebuild the boardstate corresponding to current_index
        memory.create_board(board, board.size, current_index)

        # check if this board is solved
        if board.check_finish():
            # if solved, return the path of moves which created this board
            return paths[current_index]

        # check and save all possible moves from this state
        for car_name in board.cars:
            # direction = 1 (left/up) or 2 (right/down)
            for direction in [1, 2]:
                steps_moved = 0

                # move a car as many steps as possible in the current direction (1 or 2). Save each step as a state
                while board.check_move(car_name, direction):
                    # move car by 1 step in current direction (1 or 2)
                    board.move(car_name, direction)
                    steps_moved += 1

                    # check if new board state has been visited before using memory
                    existing_index = memory.compare_boards(board.cars, car_names)
                    if existing_index is None:
                        # its a new state: save board, enqueue and record path
                        memory.save_board(board.cars, car_names)
                        new_index = len(memory.saved_boards) -1

                        # new path = old path + new move
                        paths[new_index] = paths[current_index] + [(car_name, direction)] * steps_moved
                        queue.append(new_index)
                    # if state already exists in memory, skip cycle. 
                    else: pass
                
                # undo all car movements so we can explore others states
                opposite_direction = 1 if direction == 2 else 2
                for _ in range(steps_moved):
                    board.move(car_name, opposite_direction)

    # if queue is empty, no solution was found
    print("BFS: no solution found.")
    return None

def export_solution(board, board_file, solution_moves):
    """
    After BFS the output_data list of the current Data class does contain all moves made by the algorithm.
    To extract the shortest path from the algorithm we have to extract the tuples containing the moves from the list paths,
    which got returned by bfs_solve()
    """

    size = board.size

    if solution_moves == None:
        return None

    data_correct_path = Data()
    board_correct_path = Board(board_file, size, data_correct_path)
        
    for (car_name, direction) in solution_moves:
        board_correct_path.move(car_name, direction)

    board_correct_path.move('X',2)

    board_correct_path.data.export_moves("solutions/breadth-first-search/output.csv")


def print_solution(board, n, input_file = 'solutions/breadth-first-search/output.csv'):
    """
    Prints a user friendly list containing the solution in the terminal
    """

    print(f'solution found in {n} moves\n')

    # reads csv file containing the solution and prints each move in a user friendly text
    with open(input_file, mode='r') as file:
        input_file = csv.reader(file)
        next(input_file)  # skip the header

        for row in input_file:
            car, move = row[0], abs(int(row[1]))
            car_object = board.cars[car]
            if move < 0 and car_object.orientation == "H":
                print(f'{car} {move} naar links')
            elif move < 0 and car_object.orientation == "V":
                print(f'{car} {move} naar boven')
            elif move > 0 and car_object.orientation == "H":
                print(f'{car} {move} naar rechts')
            elif move > 0 and car_object.orientation == "V":
                print(f'{car} {move} naar beneden')

def breadth_first_search(board, memory, board_file):
    """
    run the breadth-first-search algorithm
    - exports the solution to "solutions/breadth-first-search/output.csv
    """

    # perform breadth first search: returns the shortest solution path
    solution = bfs_solver(board, memory)

    # export the solution into a csv
    export_solution(board, board_file, solution)

    # shorten the csv list by combining consecutive moves
    n = combine_moves("solutions/breadth-first-search/output.csv", "solutions/breadth-first-search/output.csv")

    # print user friendly solution in terminal
    print_solution(board, n)