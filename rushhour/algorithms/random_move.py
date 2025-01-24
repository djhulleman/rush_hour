import random

def random_solve(board):
    '''algorithm that takes random steps to solve the puzzle'''
    # create object for car that needs to get out
    XX = board.cars["X"] 
    complete = False
    n = 0
    save_car = ''
    save_move = ''
    # Prevent infinite loops
    max_iterations = 10000000

    while not complete and n < max_iterations:
        # chose random car and random direction
        random_car = random.choice(list(board.cars.keys()))  
        random_move = random.choice([1, 2])
        # move the car if possible
        if board.check_move(random_car, random_move):
            board.move(random_car, random_move)
            # make sure staps are counted correctly
            if save_car == random_car and save_move == random_move:
                pass
            else:
                n += 1
            save_move = random_move
            save_car = random_car
            print(f"Move {n}: Car {random_car} moved {'left/up' if random_move == 1 else 'right/down'}")
        # check if the red car is at the end
        complete = board.check_finish()

    if complete:
        print(f"Puzzle solved in {n} moves!")
        board.print()
        return n
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")
