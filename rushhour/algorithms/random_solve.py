import random
import matplotlib.pyplot as plt
from matplotlib import patches

def random_solve(board):
    """Algorithm that takes random steps to solve the puzzle."""
    # Create object for the car that needs to get out
    XX = board.cars["X"] 
    complete = False
    n = 0
    # Prevent infinite loops
    max_iterations = 10000000

    # Set up the dynamic plotting
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.ion()  # Enable interactive mode

    while not complete and n < max_iterations:
        # Choose a random car and a random direction
        random_car = random.choice(list(board.cars.keys()))  
        random_move = random.choice([1, 2])
        # Move the car if possible
        board.move(random_car, random_move)
        n += 1
        print(f"Move {n}: Car {random_car} moved {'left/up' if random_move == 1 else 'right/down'}")

        # Check if the red car is at the end
        complete = board.check_finish()

    plt.ioff()  # Disable interactive mode
    plt.show()  # Display the final board

    if complete:
        print(f"Puzzle solved in {n} moves!")
        board.print()
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")