from rushhour.classes.memory import *

def random_with_memory(board, memory):

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

        board.move(random_car, random_move)

        comparison_result = memory.compare_boards(board.cars, car_names)
        if comparison_result is not None:

            n = comparison_result
            memory.create_board(board, size, n)

            boards_to_remove = memory.saved_boards[n+1:] 
            for boardt in boards_to_remove:
                h = memory.hash_board(boardt, car_names)
                memory.board_hashes.pop(h, None)

            del memory.saved_boards[n+1:]
            board.data.del_moves(n)

        else: 
            memory.save_board(board.cars, car_names)
            n += 1

        s += 1
        complete = board.check_finish()
        if s%10000 == 0:
            print(f"loading, {s} steps")

    if complete:
        print(f"Puzzle solved in {n} moves!")
        return board
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")