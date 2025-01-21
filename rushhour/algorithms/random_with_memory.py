from rushhour.classes.memory import *

def random_with_memory(board, memory, items = 0):

    size = board.size
    car_names = board.cars.keys()
    data = board.data
    car_list = list(car_names)

    memory.save_board(board.cars, car_names)
        
    complete = False
    n = items
    s = items
    max_iterations = 10000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

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
            n += 1

        s += 1
        complete = board.check_finish()
        # if s%50000 == 0:
            # print(f"loading, {s} steps")

    if complete:
        n += 1 # Last step is made inside board.check_finish()
        print(f"Puzzle solved in {n} moves!")
        return data, n
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")