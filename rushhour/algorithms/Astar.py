import heapq
import copy
import itertools
from rushhour.classes.data import Data
from rushhour.classes.memory import Memory
from rushhour.classes.car import Car

# Create a unique counter for tie-breaking
counter = itertools.count()

def A_Star(board, memory, heuristic_type=0):
    """
    A* algorithm for solving the Rush Hour puzzle using the Memory class.
    """
    # Initialize a Data object to store the moves
    data = Data()
    board.data = data  # Link the board's data to this instance

    # Priority queue for A* (priority, counter, board object)
    queue = []
    heapq.heappush(queue, (0, next(counter), board))

    # Use the Memory class to track visited states
    car_names = list(board.cars.keys())  # List of all car names

    while queue:
        # Get the board with the lowest cost
        _, _, current_board = heapq.heappop(queue)

        # Save the current board state in memory and check if it's already visited
        if memory.compare_boards(current_board.cars, car_names) is not None:
            continue  # Skip already visited states

        memory.save_board(current_board.cars, car_names)  # Save this new state in memory

        # Check if we reached the goal
        if current_board.check_finish():
            # Export the moves when the solution is found
            current_board.data.export_moves("solutions/output.csv")
            return current_board  # Solution found

        # Generate children and add them to the queue
        children = generate_children(current_board)
        for child in children:
            # Check if the child state is already visited using the Memory class
            if memory.compare_boards(child.cars, car_names) is None:
                g = len(current_board.history)  # Cost-so-far
                if heuristic_type == 0:
                    h = blocking_cars_heuristic(child)  # Heuristic estimate
                elif heuristic_type == 1:
                    h = moves_needed_heuristic(child)  # Heuristic estimate
                elif heuristic_type == 2:
                    h = improved_heuristic(child)  # Heuristic estimate
                else:
                    raise ValueError("Invalid heuristic type")

                # Add the child state to the priority queue
                heapq.heappush(queue, (g + h, next(counter), child))

    # If no solution is found
    print("No solution found.")
    return None


def generate_children2(board, memory):
    """
    Generates all possible child states (boards) from the given board state.
    Ensures no duplicate states are added to the memory or children list.
    Does not use deep copies of the board, instead reverts moves after exploration.
    """
    children = []
    car_names = board.cars.keys()

    for car_name in board.cars:
        for direction in [1, 2]:
            steps_moved = 0  # Count how many steps were successfully moved

            while board.check_move(car_name, direction):
                # Move the car in the specified direction
                board.move(car_name, direction)
                steps_moved += 1

                # Check if the current state is new
                if memory.compare_boards(board.cars, car_names) is None:
                    memory.save_board(board.cars, car_name)  # Save the new state
                    children.append(copy.deepcopy(board))  # Add to children

            # Revert the car to its original position
            opposite_direction = 1 if direction == 2 else 2
            for _ in range(steps_moved):
                board.move(car_name, opposite_direction)

    return children


def generate_children(board):
    """
    Generates all possible next states (children) from the current board state,
    including moves that require multiple steps.
    """
    children = []
    for car in board.cars.values():
        if car.orientation == "H":
            steps = 1
            while board.check_move(car.car, 1, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1, steps)
                children.append(child_board)
                steps += 1
            steps = 1
            while board.check_move(car.car, 2, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2, steps)
                children.append(child_board)
                steps += 1
        elif car.orientation == "V":
            steps = 1
            while board.check_move(car.car, 1, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1, steps)
                children.append(child_board)
                steps += 1
            steps = 1
            while board.check_move(car.car, 2, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2, steps)
                children.append(child_board)
                steps += 1
    return children


def blocking_cars_heuristic(board):
    """
    Heuristic function to estimate the cost to reach the goal.
    Measures the number of cars blocking the path of the X car.
    """
    x_car = board.cars['X']
    blocks = 0
    for col in range(x_car.col + x_car.length - 1, board.size):
        if board.board[x_car.row - 1][col] != '_':  # Blocking cars
            blocks += 1
    return blocks


def moves_needed_heuristic(board):
    """
    Heuristic function that calculates the minimum number of moves needed for all cars
    to allow the "X" car to exit.
    """
    x_car = board.cars['X']
    total_moves = 0

    # Target column: the exit column for the "X" car
    target_col = board.size

    # Check the path of the "X" car to the exit
    for col in range(x_car.col + x_car.length - 1, target_col):
        # If there's a car blocking the path
        blocking_car = board.board[x_car.row - 1][col]
        if blocking_car != '_':
            blocking_car_obj = board.cars[blocking_car]
            if blocking_car_obj.orientation == "H":
                moves_left = blocking_car_obj.col - 1
                moves_right = board.size - (blocking_car_obj.col + blocking_car_obj.length - 1)
                total_moves += min(moves_left, moves_right)
            elif blocking_car_obj.orientation == "V":
                moves_up = blocking_car_obj.row - 1
                moves_down = board.size - (blocking_car_obj.row + blocking_car_obj.length - 1)
                total_moves += min(moves_up, moves_down)
    return total_moves


def improved_heuristic(board):
    """
    An improved heuristic to estimate the cost to solve the puzzle.
    Calculates the number of blocking cars and the cost to move them.
    """
    x_car = board.cars['X']
    blocking_cost = 0

    # Check all cars directly blocking the X car
    for col in range(x_car.col + x_car.length - 1, board.size):
        blocking_car = board.board[x_car.row - 1][col]
        if blocking_car != '_':  # Found a blocking car
            if isinstance(blocking_car, str):
                blocking_car_obj = board.cars[blocking_car]
            elif isinstance(blocking_car, Car):
                blocking_car_obj = blocking_car
            else:
                continue  # Skip empty or invalid cells

            # Calculate the cost to move the blocking car out of the way
            if blocking_car_obj.orientation == 'H':
                blocking_cost += (blocking_car_obj.col + blocking_car_obj.length - 1 - col)
            elif blocking_car_obj.orientation == 'V':
                blocking_cost += (blocking_car_obj.row + blocking_car_obj.length - 1 - x_car.row)

    return blocking_cost




