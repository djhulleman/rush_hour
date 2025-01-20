from rushhour.classes.memory import *

def random_with_memory_and_backtracking(board, memory):
    # Step 1: Solve the board using Random with Memory
    size = board.size
    car_names = board.cars.keys()
    car_list = list(car_names)

    memory.save_board(board.cars, car_names)
        
    complete = False
    n = 0
    s = 0
    max_iterations = 1000000  # Prevent infinite loops

    while not complete and n < max_iterations:
        random_car = random.choice(car_list)
        random_move = random.choice([1, 2])

        board.move(random_car, random_move)

        comparison_result = memory.compare_boards(board.cars, car_names)
        if comparison_result is not None:
            n = comparison_result
            memory.create_board(board, size, n)

            # Delete saved hashes, boards, and moves
            memory.del_hashes(memory, n, car_names)
            del memory.saved_boards[n+1:]
            board.data.del_moves(n)
        else: 
            memory.save_board(board.cars, car_names)
            n += 1

        s += 1
        complete = board.check_finish()

    if not complete:
        print("Failed to solve the puzzle within the maximum number of iterations.")
        return

    print(f"Puzzle solved in {n} moves!")

    # Step 2: Backtrack to remove redundant moves
    print("Starting backtracking to remove redundant moves...")
    optimized_moves = n  # Start with total moves

    last_board = memory.saved_boards[-1]
    for step in range(len(memory.saved_boards) - 2, -1, -1):
        current_board = memory.saved_boards[step]

        # Compare current board with last board
        if memory.hash_board(current_board, car_names) == memory.hash_board(last_board, car_names):
            print(f"Duplicate board found at step {step}. Removing redundant moves...")
            optimized_moves = step
            board.data.del_moves(step)
            memory.del_hashes(memory, step, car_names)
            del memory.saved_boards[step+1:]

        last_board = current_board

    print(f"Backtracking complete. Puzzle solved in {optimized_moves} optimized moves.")
    board.data.export_moves("solutions/output.csv")
