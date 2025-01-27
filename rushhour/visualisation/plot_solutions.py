import matplotlib.pyplot as plt
import random
import csv

from rushhour.visualisation.UserInterface import draw_board_dynamic
from rushhour.classes.board import Board
from rushhour.classes.data import Data


def plot_solution(board_file, solution_file):
    size = int(board_file[-7])  # Assuming board size is encoded in the filename
    data = Data()
    board = Board(board_file, size, data)
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(6, 6))

    # Assign random colors to cars
    car_colors = {}
    for car in board.cars.values():
        if car.car not in car_colors:                
            car_colors[car.car] = 'red' if car.car == 'X' else f"#{random.randint(0, 0xFFFFFF):06x}"

    # Initial draw of the board
    draw_board_dynamic(board, ax, car_colors)

    with open(solution_file, mode='r') as file:
        csvFile = csv.reader(file)
        # Skip the header
        next(csvFile)
        for i, lines in enumerate(csvFile):
            try:
                car = lines[0]
                move = int(lines[1])
                if move == -1:
                    move = 1
                else:
                    move = 2
                # Check and execute the move
                if board.check_move(car, move):
                    board.move(car, move)
                    print(f"Move {i + 1}: Car {car} moved {'left/up' if move < 0 else 'right/down'}")
                    # Update the plot dynamically
                    ax.clear()
                    draw_board_dynamic(board, ax, car_colors)
                else:
                    print(f"Move {i + 1}: Invalid move for car {car}: {move}")
            except (IndexError, ValueError) as e:
                print(f"Error processing line {i + 1}: {lines} - {e}")

    # Wait for user input to close the plot
    input("Press Enter to continue...")
    plt.close()