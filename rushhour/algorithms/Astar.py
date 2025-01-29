import heapq
import copy
import itertools
from rushhour.classes.data import Data

# Create a unique counter for tie-breaking in the priority queue
counter = itertools.count()

def A_Star(board, heuristic_type=0):
    """
    heuristic_type = 0 -> blocking_cars_heuristic
    heuristic_type = 1 -> moves_needed_heuristic
    heuristic_type = 2 -> tiered_blocking_heuristic
    """
    # Initialize priority queue for A* (f, counter, board)
    queue = []

    # The cost-so-far (g) for the initial board is 0, so priority = g + h.
    heapq.heappush(queue, (0, next(counter), board))

    visited = {}

    while queue:
        # Get the board with the lowest f
        f, _, current_board = heapq.heappop(queue)

        # Check if the puzzle is solved
        if current_board.check_finish():
            # Export the moves when the solution is found
            current_board.data.export_moves("solutions/output.csv")
            return current_board

        # Compute cost so far for the current board
        current_g = len(current_board.history)
        current_hash = hash_board_state(current_board)

        # Skip if we've visited this exact state with equal or lower cost
        if current_hash in visited and visited[current_hash] <= current_g:
            continue

        # Record that we've now found this state with cost
        visited[current_hash] = current_g

        # Generate possible next children
        children = generate_children(current_board)

        for child in children:
            child_g = len(child.history)
            child_hash = hash_board_state(child)

            # If we've never seen this child or we found or cheaper 
            if child_hash not in visited or child_g < visited[child_hash]:

                # Choose the heuristic based on user selection
                h = blocking_cars_heuristic(child)

                # f = g + h
                heapq.heappush(queue, (child_g + h, next(counter), child))

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


def hash_board_state(board):
    """
    Returns a hashable integer for the board's state,
    based on each car's (row, col) position.
    """
    hash_value = 0
    for car in board.cars.values():
        # Combine row & col into a single integer
        hash_value = hash_value * 31 + (car.row * board.size + car.col)
    return hash_value

def generate_children(board):
    """
    Generates all possible next states (children) from the current board state,
    including multi-step moves for each car.
    """
    children = []

    for car in board.cars.values():
        if car.orientation == "H":
            # Try moving left by multiple steps
            steps = 1
            while board.check_move(car.car, 1, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1, steps)

                # IMPORTANT: Update the child's history to reflect this move
                child_board.history = board.history + [(car.car, 1, steps)]

                children.append(child_board)
                steps += 1

            # Try moving right by multiple steps
            steps = 1
            while board.check_move(car.car, 2, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2, steps)

                # Update the child's history
                child_board.history = board.history + [(car.car, 2, steps)]

                children.append(child_board)
                steps += 1

        elif car.orientation == "V":
            # Try moving up by multiple steps
            steps = 1
            while board.check_move(car.car, 1, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1, steps)

                # Update the child's history
                child_board.history = board.history + [(car.car, 1, steps)]

                children.append(child_board)
                steps += 1

            # Try moving down by multiple steps
            steps = 1
            while board.check_move(car.car, 2, steps):
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2, steps)

                # Update the child's history
                child_board.history = board.history + [(car.car, 2, steps)]

                children.append(child_board)
                steps += 1

    return children
