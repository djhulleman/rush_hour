import heapq
import copy
import itertools
from rushhour.classes.data import Data  # Assuming Data class is in the given location

# Create a unique counter for tie-breaking
counter = itertools.count()

def A_Star(board, heuristic_type=0):
    # Initialize a Data object to store the moves
    data = Data()
    board.data = data  # Link the board's data to this instance

    # Priority queue for A* (priority, counter, board object)
    queue = []
    heapq.heappush(queue, (0, next(counter), board))

    # Set to track visited states
    visited = set()

    while queue:
        # Get the board with the lowest cost
        _, _, current_board = heapq.heappop(queue)

        # Check if we reached the goal
        if current_board.check_finish():
            # Export the moves when the solution is found
            current_board.data.export_moves("solutions/output.csv")
            return current_board  # Solution found

        # Hash current board state
        hash = hash_board_state(current_board)
        if hash in visited:
            continue  # Skip already visited states

        visited.add(hash)

        # Generate children and add them to the queue
        children = generate_children(current_board)
        for child in children:
            if hash_board_state(child) not in visited:
                g = len(current_board.history)  # Cost-so-far
                if heuristic_type == 0:
                    h = blocking_cars_heuristic(child)  # Heuristic estimate
                if heuristic_type == 1:
                    h = moves_needed_heuristic(child) # Heuristic estimate
                if heuristic_type == 2:
                    h = tiered_blocking_heuristic(child)
                heapq.heappush(queue, (g + h, next(counter), child))

    # If no solution is found
    print("No solution found.") 
    return None

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
            # Calculate moves needed to get the blocking car out of the way
            if blocking_car.orientation == "H":
                # Horizontal cars can only move left or right
                # Calculate minimum moves to clear the path
                moves_left = blocking_car.col - 1  # Spaces to the left edge
                moves_right = board.size - (blocking_car.col + blocking_car.length - 1)  # Spaces to the right edge
                total_moves += min(moves_left, moves_right)
            elif blocking_car.orientation == "V":
                # Vertical cars can only move up or down
                # Calculate minimum moves to clear the path
                moves_up = blocking_car.row - 1  # Spaces to the top edge
                moves_down = board.size - (blocking_car.row + blocking_car.length - 1)  # Spaces to the bottom edge
                total_moves += min(moves_up, moves_down)

    # Check other cars that may not block directly but need to be repositioned
    for car in board.cars.values():
        if car.car == 'X':
            continue  # Skip the X car
        # Evaluate if the car is in a position that obstructs movement
        if car.orientation == "H":
            # Horizontal cars: check if they overlap with the row of the "X" car
            if car.row == x_car.row:
                moves_left = car.col - 1
                moves_right = board.size - (car.col + car.length - 1)
                total_moves += min(moves_left, moves_right)
        elif car.orientation == "V":
            # Vertical cars: check if they block columns that need clearing
            if x_car.col <= car.col <= target_col:
                moves_up = car.row - 1
                moves_down = board.size - (car.row + car.length - 1)
                total_moves += min(moves_up, moves_down)

    return total_moves

def tiered_blocking_heuristic(board):
    """
    Heuristic function that calculates the cost based on:
    1. First-tier blocking cars: cars directly blocking the X car's path.
    2. Second-tier blocking cars: cars that block the first-tier blocking cars.
    """
    x_car = board.cars['X']
    first_tier_blocks = 0
    second_tier_blocks = 0
    exit_col = board.size  # Assume the X car exits at the far right

    # Identify first-tier blocking cars
    for col in range(x_car.col + x_car.length - 1, exit_col):
        blocking_car = board.board[x_car.row - 1][col]  # Get the cell content
        if blocking_car != '_':  # Found a blocking car
            blocking_car_id = blocking_car.car  # Get the car ID (e.g., 'A')
            first_tier_blocks += 1

            # Ensure the blocking car exists in the board.cars dictionary
            blocking_car_obj = board.cars[blocking_car_id]

            # Check if this blocking car is itself blocked
            if blocking_car_obj.orientation == "H":
                # Horizontal blocking car: check left and right for obstacles
                left_block = (
                    board.board[blocking_car_obj.row - 1][blocking_car_obj.col - 2]
                    if blocking_car_obj.col > 1
                    else '_'
                )
                right_block = (
                    board.board[blocking_car_obj.row - 1][blocking_car_obj.col + blocking_car_obj.length - 1]
                    if blocking_car_obj.col + blocking_car_obj.length <= board.size
                    else '_'
                )
                if left_block != '_':
                    second_tier_blocks += 1
                if right_block != '_':
                    second_tier_blocks += 1

            elif blocking_car_obj.orientation == "V":
                # Vertical blocking car: check up and down for obstacles
                up_block = (
                    board.board[blocking_car_obj.row - 2][blocking_car_obj.col - 1]
                    if blocking_car_obj.row > 1
                    else '_'
                )
                down_block = (
                    board.board[blocking_car_obj.row + blocking_car_obj.length - 1][blocking_car_obj.col - 1]
                    if blocking_car_obj.row + blocking_car_obj.length <= board.size
                    else '_'
                )
                if up_block != '_':
                    second_tier_blocks += 1
                if down_block != '_':
                    second_tier_blocks += 1

    # Weight the two tiers of blocking
    first_tier_weight = 5  # Weight for first-tier blocking
    second_tier_weight = 2  # Weight for second-tier blocking

    # Calculate the total heuristic cost
    return first_tier_blocks * first_tier_weight + second_tier_blocks * second_tier_weight


def hash_board_state(board):
    hash_value = 0
    for car in board.cars.values():
        hash_value = hash_value * 31 + (car.row * board.size + car.col)
    return hash_value


def generate_children(board):
    """
    Generates all possible next states (children) from the current board state.
    """
    children = []
    for car in board.cars.values():
        if car.orientation == "H":  # Horizontal car
            if board.check_move(car.car, 1):  # Check if move left is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1)
                children.append(child_board)
                
            if board.check_move(car.car, 2):  # Check if move right is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2)
                children.append(child_board)
        
        elif car.orientation == "V":  # Vertical car
            if board.check_move(car.car, 1):  # Check if move up is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1)
                children.append(child_board)
                
            if board.check_move(car.car, 2):  # Check if move down is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2)
                children.append(child_board)
    
    return children
