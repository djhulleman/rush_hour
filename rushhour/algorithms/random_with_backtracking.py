from rushhour.classes.memory import *
import random
import copy

def random_with_backtracking(board, memory):
    size = board.size
    car_names = board.cars.keys()
    car_list = list(car_names)

    memory.save_board(board.cars, car_names)
    
    complete = False
    n = 0
    s = 0
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

        # Save the move before making it
        board.data.save_move(random_car, random_move)

        # Make the move
        board.move(random_car, random_move)

        # Check for duplicate boards
        comparison_result = memory.compare_boards(board.cars, car_names)
        if comparison_result is not None:
            # Duplicate board found, backtrack
            n = comparison_result
            memory.create_board(board, size, n)

            # Clear redundant moves
            memory.del_hashes(memory, n, car_names)
            del memory.saved_boards[n+1:]

            # Delete redundant moves in the board data
            board.data.del_moves(n)

        else:
            # No duplicate, save the current board state
            memory.save_board(board.cars, car_names)
            n += 1

        s += 1
        complete = board.check_finish()

    if complete:
        n += 1  # Last step is made inside board.check_finish()
        print(f"Debug: Puzzle solved in {n} moves!")
        
        # At this point, we need to export the moves after solving.
        board.data.export_moves("solutions/output.csv")
        return board, n
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")
