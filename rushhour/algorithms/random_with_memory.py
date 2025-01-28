from rushhour.classes.memory import *

def random_with_memory(board, memory):
    """
    Solves a Rush Hour game using random moves, 
    incorperating memory to avoid redundant states.
    """

    # get board properties
    size = board.size # board size 
    car_names = board.cars.keys()
    car_list = list(car_names) # list of car names

    # save the initial board state in memory
    memory.save_board(board.cars, car_names)
        
    complete = False # used in loop condition
    n = 0 # count number of moves
    s = 0 # count total steps attempted
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        #random select a car and a movement direction
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

        # check if selected move is valid
        if board.check_move(random_car, random_move):
            # perform the actual movement of the car
            board.move(random_car, random_move)

            # compare the board state with previously saved board states
            comparison_result = memory.compare_boards(board.cars, car_names)
            if comparison_result is not None:
                
                # previous board state has been found, move back to this previous board state
                n = comparison_result
                memory.create_board(board, size, n)

                # delete saved hashes, boards and moves
                memory.del_hashes(memory, n, car_names)
                del memory.saved_boards[n+1:]
                board.data.del_moves(n)

            else:
                # its a unique board state, save in memory 
                memory.save_board(board.cars, car_names)
            n += 1 # increment move counter
            s += 1 # increment step counter

            # check if rush hour game is solved
            complete = board.check_finish()
            # if s%50000 == 0:
                # print(f"loading, {s} steps")

    # print result 
    if complete:
        print(f"Puzzle solved in {n} moves!")
        return board, n
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")