import matplotlib.pyplot as plt
from matplotlib import patches
import tkinter as tk
from tkinter import simpledialog
import csv
import random
import copy

from rushhour.classes.board import Board
from rushhour.classes.data import Data

# Import the random_solve function or other algorithms from the algorithms folder
from rushhour.algorithms.random_move import random_solve
from rushhour.algorithms.random_with_plot import solve_with_visualization
from rushhour.algorithms.random_with_memory import random_with_memory
from rushhour.algorithms.comparing import *
from rushhour.algorithms.Astar import *


def plot_board(board):
    """Plots the Rush Hour board."""
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(0, board.size)
    ax.set_ylim(0, board.size)
    ax.set_aspect('equal')

    # Draw grid
    for x in range(board.size + 1):
        ax.axhline(x, color='grey', linewidth=0.5)
        ax.axvline(x, color='grey', linewidth=0.5)

    # Draw cars
    car_colors = {}
    for car in board.cars.values():
        if car.car not in car_colors:                
            car_colors[car.car] = 'red' if car.car == 'X' else f"#{random.randint(0, 0xFFFFFF):06x}"  # Extend as needed

    for car in board.cars.values():
        if car.orientation == "H":
            x, y = car.col - 1, board.size - car.row
            width, height = car.length, 1
        else:
            x, y = car.col - 1, board.size - car.row - car.length + 1
            width, height = 1, car.length

        ax.add_patch(
            patches.Rectangle(
                (x, y), width, height,
                edgecolor='black',
                facecolor=car_colors.get(car.car, 'gray')  # Default to gray if color is missing
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
    plt.show()

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
    plt.pause(0.0001)

def plot_solution(board, solution_file):
    data = Data()
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

def visualize_and_solve(board, memory):
    """Plots the board and asks the user to choose a solving method."""
    # Plot initial board
    plot_board(board)

    # Create a simple GUI to ask for solving method
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask for the algorithm
    algorithm = simpledialog.askstring(
        "Select Algorithm",
        "Enter the solving algorithm: 1 = Random | 2 = Random with plot | 3 = Random with memory | 4 = comparing | 5 = A*",
    )

    # Solve the puzzle using the chosen algorithm
    if algorithm == "1":
        random_solve(board) 
    elif algorithm == "2":
        solve_with_visualization(board)      
    elif algorithm == "3":
        begin_state = copy.deepcopy(board)
        random_with_memory(board, memory)
        board.data.export_moves("solutions/output.csv")
        plot_solution(begin_state, "solutions/output.csv")
    elif algorithm == "4":
        begin_state = copy.deepcopy(board)
        run_comparing(board.name, board.size)
        plot_solution(begin_state, "solutions/compair_path.csv")
    elif algorithm == "5":
        heuristic = simpledialog.askstring(
        "Select Heuristic",
        "Enter the solving algorithm: 0 = blocking_cars_heuristic | 1 = moves_needed_heuristic | 2 = two_tiered_blocking_heuristic",
        )
        A_Star(board, int(heuristic))
        plot_solution(board, "solutions/output.csv")
    else:
        print("Invalid algorithm selected.")