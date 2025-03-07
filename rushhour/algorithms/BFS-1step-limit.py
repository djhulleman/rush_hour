from collections import deque
from rushhour.algorithms.shorten_csv import combine_moves
import csv
import time

def bfs_solver(board, memory):
    """
    Perform a BFS to find the shortest solution.
    This algorithm limits the maximum step per car to 1. 
    This will change the shape and search sequence of the state-space.
    """
    # save the initial state in memory and save its index
    car_names = board.cars.keys()
    memory.save_board(board.cars, car_names)
    start_index = len(memory.saved_boards) - 1

    # use a queue of indices linked to memory.saved_boards 
    queue = deque([start_index])

    # keep track of paths:  paths[state_index] = list of moves from start
    paths = {start_index: []}

    while queue:
        current_index = queue.popleft()
        
        # rebuild that board state
        memory.create_board(board, board.size, current_index)

        # check if game is solved
        if board.check_finish():
            # if solved, return the path of moves
            return paths[current_index]

        # check and save all possible single moves from this state
        for car_name in board.cars:
            # direction = 1 (left/up) or 2 (right/down)
            for direction in [1, 2]:
                # check if move is valid
                if board.check_move(car_name, direction):
                    # if valid, make the move
                    board.move(car_name, direction)

                    # check if new board state has been visited before
                    existing_index = memory.compare_boards(board.cars, car_names)
                    if existing_index is None:
                        # it is a new state: save board, enqueue and record path
                        memory.save_board(board.cars, car_names)
                        new_index = len(memory.saved_boards) - 1

                        paths[new_index] = paths[current_index] + [(car_name, direction)]
                        queue.append(new_index)
                    else:
                        # we have already visited this state, skipp this cycle 
                        pass

                    # 6) undo the move (opposite direction) so we can keep expanding
                    opposite = 1 if direction == 2 else 2
                    board.move(car_name, opposite)

    # if queue is empty, no solution was found
    print("BFS: no solution found.")
    return None

def export_solution(solution_moves):
    """
    After BFS the output_data list of the Data class does contain all moves made by the algorithm.
    To extract the shortest path from the algorithm we have to extract the tuples containing the moves from the list paths,
    which got returned by bfs_solve()
    """

    if solution_moves == None:
        return

    data_correct_path = Data()
    board_correct_path = Board(board_file, size, data_correct_path)
        
    for (car_name, direction) in solution_moves:
        board_correct_path.move(car_name, direction)

    board_correct_path.move('X',2)

    board_correct_path.data.export_moves()


def print_solution(board, n, input_file = 'output.csv'):
    print(f'solution found in {n} moves\n')

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

def breadth_first_search(board, memory):

    # perform breadth first search: returns the list with moves
    solution = bfs_solver(board, memory)

    # export the moves into a csv
    export_solution(solution)
    # shorten the csv list by combining consecutive moves
    n = combine_moves()
    # print solution in terminal
    print_solution(board, n)

if __name__ == "__main__":
 
    from rushhour.classes.board import Board
    from rushhour.classes.memory import Memory
    from rushhour.classes.data import Data

    # For example, load a 6x6 puzzle from a CSV:
    data = Data()
    memory = Memory()
    size = 9
    board_file = "../../gameboards/Rushhour9x9_5.csv"  # or "Rushhour6x6_1.csv", etc.
    board = Board(board_file, size, data)

    start_time = time.time()

    breadth_first_search(board, memory)

    end_time = time.time()
    duration = end_time - start_time
 
    print(f'Algorithm took: {duration}')
