import matplotlib.pyplot as plt
import matplotlib.pyplot as patches

def draw_board_dynamic(board, ax, car_colors):
    '''Graphically update the Rush Hour board dynamically during each move'''
    # Clear the previous board state
    ax.clear()
    ax.set_xlim(0, board.size)
    ax.set_ylim(0, board.size)
    ax.set_aspect('equal')

    # Draw grid
    for x in range(board.size + 1):
        ax.axhline(x, color='grey', linewidth=0.5)
        ax.axvline(x, color='grey', linewidth=0.5)

    # Draw cars
    for car in board.cars.values():
        # Horizontal cars
        if car.orientation == "H":
            x, y = car.col - 1, board.size - car.row
            width, height = car.length, 1
        # Vertical cars
        else:
            x, y = car.col - 1, board.size - car.row - car.length + 1
            width, height = 1, car.length

        ax.add_patch(
            patches.Rectangle(
                (x, y), width, height,
                edgecolor='black',
                facecolor=car_colors[car.car]
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
    # Pause to make the animation smooth
    plt.pause(0.000001)