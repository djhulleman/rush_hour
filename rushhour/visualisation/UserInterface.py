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
from rushhour.classes.memory import Memory

# Import the random_solve function or other algorithms from the algorithms folder
from rushhour.algorithms.random_move import *
from rushhour.algorithms.random_with_plot import solve_with_visualization
from rushhour.algorithms.random_with_memory import random_with_memory
from rushhour.algorithms.comparing import *
from rushhour.algorithms.Astar import *
from rushhour.algorithms.BFS import *
from rushhour.algorithms.hillclimber import *

def UserInterface():
    """Create the initial window to choose a game board."""
    def select_board(size, game):
        size = int(size)
        board_file = f"gameboards/Rushhour{size}x{size}_{game}.csv"
        memory = Memory()
        board = Board(board_file, size)
        root.destroy()  # Close the start window
        visualize_and_solve(board, memory)

    root = tk.Tk()
    root.title("Select Game Board")
    root.geometry("400x400")  # Set window size

    # Label for instructions
    tk.Label(root, text="Select a Rush Hour board:", font=("Arial", 14)).pack(pady=20)

    # Add buttons for board sizes
    board_options = [
        ("6x6_1", "6", "1"),
        ("6x6_2", "6", "2"),
        ("6x6_3", "6", "3"),
        ("9x9_4", "9", "4"),
        ("9x9_5", "9", "5"),
        ("9x9_6", "9", "6"),
        ("12x12_7", "12", "7"),
    ]
    
    for board_name, size, game in board_options:
        tk.Button(root, text=board_name, command=lambda size=size, game=game: select_board(size, game)).pack(fill="x", padx=20, pady=5)

    # Start the GUI event loop
    root.mainloop()

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

# Other methods: draw_board_dynamic, plot_solution, count_moves, visualize_and_solve, etc. (unchanged)

def visualize_and_solve(board, memory):
    """Plots the board and provides a GUI with buttons for choosing a solving method."""
    
    def run_algorithm(algorithm):
        """Runs the selected algorithm."""
        if algorithm == "1":
            random_move(board)
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
            compare = Comparing(board.name, board.size)
            outcome = compare.run_comparing()
            outcome.export_moves("solutions/compair_path.csv")
            plot_solution(begin_state, "solutions/compair_path.csv")
            root.destroy()
        elif algorithm == "5":
            A_Star(board)
            plot_solution(board, "solutions/output.csv")
        elif algorithm == "6":
            load_solution_file()  # Open file selection for existing solution
            root.destroy()
        elif algorithm == "7":
            start = deepcopy(board)
            solution = bfs_solver(board, memory)
            export_solution(board, board.name, solution)
            plot_solution(start, "solutions/breadth-first-search/output.csv")

        elif algorithm == "8":
            hillclimber(board.size, board.name[-5])
        else:
            messagebox.showerror("Error", "Invalid algorithm selected.")

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
    tk.Button(root, text="7. BFS", command=lambda: run_algorithm("7")).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="8. Hillclimber", command=lambda: run_algorithm("8")).pack(fill="x", padx=20, pady=5)

    # Start the GUI event loop
    root.mainloop()

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
                    plt.pause(0.001)  # Pause for animation effect
                else:
                    print(f"Move {i + 1}: Invalid move for car {car}: {move}")
            except (IndexError, ValueError) as e:
                print(f"Error processing line {i + 1}: {lines} - {e}")

    # Wait for user input to close the plot
    input("Press Enter to continue...")
    plt.close()