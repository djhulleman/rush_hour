import matplotlib.pyplot as plt
from matplotlib import patches
import tkinter as tk
from tkinter import simpledialog
import csv
import random
import copy
from tkinter import messagebox



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
    fig, ax = plt.subplots(figsize=(6, 6))
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
    plt.pause(0.00001)


def plot_solution(board, solution_file):
    """
    Visualizes the solution for the board by reading a solution file
    and animating the moves dynamically.
    """
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

                # Determine the direction and steps
                if move < 0:
                    direction = 1  # Left or Up
                    steps = -move
                else:
                    direction = 2  # Right or Down
                    steps = move

                # Check and execute the move
                if board.check_move(car, direction, steps):
                    board.move(car, direction, steps)
                    print(f"Move {i + 1}: Car {car} moved {'left/up' if direction == 1 else 'right/down'} by {steps} steps")

                    # Update the plot dynamically
                    ax.clear()
                    draw_board_dynamic(board, ax, car_colors)
                    plt.pause(0.5)  # Pause for animation effect
                else:
                    print(f"Move {i + 1}: Invalid move for car {car}: {move}")
            except (IndexError, ValueError) as e:
                print(f"Error processing line {i + 1}: {lines} - {e}")

    # Wait for user input to close the plot
    input("Press Enter to continue...")
    plt.close()

def count_moves(filename):
    total_moves = 0
    last_car = None
    move_block = False  # Track if the current car's move is already counted

    # Open and read the file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            car, move = row
            # If the current car is not the same as the last car, reset the move block
            if car != last_car:
                move_block = False

            # Count the move only if it's not part of a block for the same car
            if not move_block:
                total_moves += 1
                move_block = True  # Mark the car's moves as counted for the block

            # Update the last car
            last_car = car

    return total_moves

def visualize_and_solve(board, memory):
    """Plots the board and provides a GUI with buttons for choosing a solving method."""
    
    def run_algorithm(algorithm):
        """Runs the selected algorithm."""
        if algorithm == "1":
            random_solve(board)
            root.destroy()
        elif algorithm == "2":
            solve_with_visualization(board)
            root.destroy()
        elif algorithm == "3":
            begin_state = copy.deepcopy(board)
            random_with_memory(board, memory)
            board.data.export_moves("solutions/output.csv")
            plot_solution(begin_state, "solutions/output.csv")
            root.destroy()
        elif algorithm == "4":
            begin_state = copy.deepcopy(board)
            run_comparing(board.name, board.size)
            plot_solution(begin_state, "solutions/compair_path.csv")
            root.destroy()
        elif algorithm == "5":
            select_heuristic()  # Open heuristic selection
            # Do not destroy root here; heuristic window handles it
        elif algorithm == "6":
            load_solution_file()  # Open file selection for existing solution
            root.destroy()
        else:
            messagebox.showerror("Error", "Invalid algorithm selected.")


    def select_heuristic():
        """Opens a new window to select a heuristic for A*."""
        heuristic_window = tk.Toplevel(root)
        heuristic_window.title("Select Heuristic")
        
        def run_a_star(heuristic):
            A_Star(board, memory, int(heuristic))
            plot_solution(board, "solutions/output.csv")
            heuristic_window.destroy()
        
        tk.Label(heuristic_window, text="Select a heuristic:").pack(pady=10)
        tk.Button(heuristic_window, text="Blocking Cars Heuristic", command=lambda: run_a_star(0)).pack(fill="x", padx=20, pady=5)
        tk.Button(heuristic_window, text="Moves Needed Heuristic", command=lambda: run_a_star(1)).pack(fill="x", padx=20, pady=5)
        tk.Button(heuristic_window, text="Two-Tiered Blocking Heuristic", command=lambda: run_a_star(2)).pack(fill="x", padx=20, pady=5)

    def load_solution_file():
        """Prompts the user to input the solution file."""
        solution_file = simpledialog.askstring("Enter Solution File", "Enter the solution file path:")
        if solution_file:
            plot_solution(board, solution_file)

    # Initialize the main GUI window
    root = tk.Tk()
    root.title("Rush Hour Solver")
    root.geometry("600x600")  # Set window size
    
    # Add a label at the top
    tk.Label(root, text="Select a solving algorithm:", font=("Arial", 14)).pack(pady=10)
    
    # Add buttons for each algorithm
    tk.Button(root, text="1. Random", command=lambda: run_algorithm("1")).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="2. Random with Plot", command=lambda: run_algorithm("2")).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="3. Random with Memory", command=lambda: run_algorithm("3")).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="4. Compare Methods", command=lambda: run_algorithm("4")).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="5. A* Algorithm", command=lambda: run_algorithm("5")).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="6. Plot Existing Solution", command=lambda: run_algorithm("6")).pack(fill="x", padx=20, pady=5)
    
    # Start the GUI event loop
    root.mainloop()
