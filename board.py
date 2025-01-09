import matplotlib.pyplot as plt
import matplotlib.patches as patches
from game import *

size = 6
game = 1

# create game board and show it
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size)
board.print()

def draw_board(board):
    '''Graphically visualize the Rush Hour board'''

    fig, ax = plt.subplots(figsize=(6, 6))
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
            x, y = car.col - 1, board.size - car.row -1
            width, height = 1, car.length

        ax.add_patch(
            patches.Rectangle(
                (x, y), width, height, edgecolor='black', facecolor='gray' if car.car != 'X' else 'red'
            )
        )
        ax.text(x + width / 2, y + height / 2, car.car, color='white', ha='center', va='center')

    ax.set_xticks(range(board.size + 1))
    ax.set_yticks(range(board.size + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(left=False, bottom=False)
    ax.set_frame_on(False)

    plt.show(block=False)  # Non-blocking mode
    input("Press Enter to continue...")  # Wait for user confirmation
    plt.close()


draw_board(board)

