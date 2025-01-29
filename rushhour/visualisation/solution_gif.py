import imageio
import numpy as np
import matplotlib.pyplot as plt
import csv
import random

from rushhour.visualisation.UserInterface import draw_board_dynamic

def plot_solution_to_gif(board, solution_file, output_gif="solution_animation.gif"):
    """Save solution animation as GIF."""
    images = []
    car_colors = {car.car: 'red' if car.car == 'X' else f"#{random.randint(0, 0xFFFFFF):06x}" for car in board.cars.values()}
    
    with open(solution_file, mode='r') as file:
        csvFile = csv.reader(file)
        next(csvFile)
        for line in csvFile:
            fig, ax = plt.subplots(figsize=(6, 6))

            # Capture the initial state of the board
            ax.clear()
            draw_board_dynamic(board, ax, car_colors)
            plt.pause(0.01)  # Small pause to update the plot

            # Capture plot as an image
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_argb(), dtype='uint8')  # Changed here
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # 4 for ARGB
            image = image[..., 1:4]  # Convert from ARGB to RGB
            images.append(image)

            # Apply the move for the next frame based on the current solution file
            car, move = line
            move = int(move)
            direction = 1 if move < 0 else 2
            steps = abs(move)
            if board.check_move(car, direction, steps):
                board.move(car, direction, steps)

            plt.close(fig)

    # Save all images as GIF
    imageio.mimsave(output_gif, images, fps=2)  # Adjust fps to control speed
    print(f"GIF saved to {output_gif}")