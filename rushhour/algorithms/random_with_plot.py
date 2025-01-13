import matplotlib.pyplot as plt
from rushhour.visualisation.dynamic_board_draw import draw_board_dynamic
import random

def solve_with_visualization(board):
    '''Algorithm that takes random steps to solve the puzzle with dynamic visualization'''

    # Create object for car that needs to get out
    XX = board.cars["X"] 
    complete = False
    n = 0
    # Prevent infinite loops
    max_iterations = 100000

    # Initialize the plot
    fig, ax = plt.subplots(figsize=(6, 6))

    # Assign random colors to cars
    car_colors = {}
    for car in board.cars.values():
        if car.car not in car_colors:
            car_colors[car.car] = 'red' if car.car == 'X' else f"#{random.randint(0, 0xFFFFFF):06x}"

    # Initial draw of the board
    draw_board_dynamic(board, ax, car_colors)

    while not complete and n < max_iterations:
        # Choose random car and random direction
        random_car = random.choice(list(board.cars.keys()))  
        random_move = random.choice([1, 2])

        # Move the car if possible
        if board.check_move(random_car, random_move):
            board.move(random_car, random_move)
            n += 1
            print(f"Move {n}: Car {random_car} moved {'left/up' if random_move == 1 else 'right/down'}")
            # Update the board visualization dynamically
            draw_board_dynamic(board, ax, car_colors)


        # Check if the "X" car can exit
        if XX.col == board.size - 2 and board.board[XX.row - 1][board.size - 1] == '_':
            complete = True

    if complete:
        print(f"Puzzle solved in {n+1} moves!")
        board.move('X', 2)
        draw_board_dynamic(board, ax, car_colors)
        board.print()
    else:
        print("Failed to solve the puzzle within the maximum number of iterations.")

    input("Press Enter to continue...") 
    plt.close()