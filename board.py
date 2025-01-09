import matplotlib.pyplot as plt
import matplotlib.patches as patches
from game import *
from data import *
import random
import time

def draw_board_dynamic(board, ax, car_colors):
    '''Graphically update the Rush Hour board dynamically during each move'''

    ax.clear()  # Clear the previous board state
    ax.set_xlim(0, board.size)
    ax.set_ylim(0, board.size)
    ax.set_aspect('equal')

    # Draw grid
    for x in range(board.size + 1):
        ax.axhline(x, color='grey', linewidth=0.5)
        ax.axvline(x, color='grey', linewidth=0.5)

    # Draw cars
    for car in board.cars.values():
        if car.orientation == "H":
            x, y = car.col - 1, board.size - car.row
            width, height = car.length, 1
        else:
            x, y = car.col - 1, board.size - car.row - 1
            width, height = 1, car.length

        ax.add_patch(
            patches.Rectangle(
                (x, y), width, height,
                edgecolor='black',
                facecolor=car_colors[car.car]  # Use assigned color
            )
        )
        ax.text(
            x + width / 2, y + height / 2, car.car,
            color='white', ha='center', va='center', fontsize=10
        )

    ax.set_xticks(range(board.size + 1))
    ax.set_yticks(range(board.size + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(left=False, bottom=False)
    ax.set_frame_on(False)
    plt.pause(0.000001)  # Pause to make the animation smooth


def solve_with_visualization(board):
    '''Algorithm that takes random steps to solve the puzzle with dynamic visualization'''

    # Create object for car that needs to get out
    XX = board.cars["X"] 
    complete = False
    n = 0
    max_iterations = 100000  # Prevent infinite loops

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



size = 12
game = 7
data = Data()
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

solve_with_visualization(board)

