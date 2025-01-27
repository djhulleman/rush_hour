import heapq
import copy
import itertools
from rushhour.classes.data import Data

# Create a unique counter for tie-breaking in the priority queue
counter = itertools.count()

def A_Star(board, heuristic_type=0):
    """
    Runs an A* search on the given Rush Hour board.
    heuristic_type = 0 -> blocking_cars_heuristic
    heuristic_type = 1 -> moves_needed_heuristic
    heuristic_type = 2 -> tiered_blocking_heuristic
    """
    # Initialize a Data object to store the moves
    data = Data()
    board.data = data  # Link the board's data to this instance

    # Initialize priority queue for A* (f, counter, board)
    queue = []
    # The cost-so-far (g) for the initial board is 0, so priority = g + h.
    # We'll compute h below before pushing. For now, do h=0 as a placeholder.
    heapq.heappush(queue, (0, next(counter), board))

    # Instead of a simple set, keep track of the best cost encountered so far
    visited = {}

    while queue:
        # Get the board with the lowest f (cost + heuristic)
        f, _, current_board = heapq.heappop(queue)

        # Check if the puzzle is solved
        if current_board.check_finish():
            # Export the moves when the solution is found
            current_board.data.export_moves("output.csv")
            return current_board  # Return the winning board

        # Compute cost so far for the current board
        current_g = len(current_board.history)
        current_hash = hash_board_state(current_board)

        # If we've visited this exact state with an equal or lower cost, skip
        if current_hash in visited and visited[current_hash] <= current_g:
            continue

        # Record that we've now found this state with cost current_g
        visited[current_hash] = current_g

        # Generate possible next states (children)
        children = generate_children(current_board)

        for child in children:
            # g for child is length of child's history
            child_g = len(child.history)
            child_hash = hash_board_state(child)

            # If we've never seen this child or we found a cheaper way to reach it
            if child_hash not in visited or child_g < visited[child_hash]:
                # Choose the heuristic based on user selection
                if heuristic_type == 0:
                    h = blocking_cars_heuristic(child)
                elif heuristic_type == 1:
                    h = moves_needed_heuristic(child)
                else:  # heuristic_type == 2
                    h = tiered_blocking_heuristic(child)

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

def moves_needed_heuristic(board):
    """
    Heuristic that calculates an approximate number of moves 
    required to clear the path for the 'X' car to exit.
    """
    x_car = board.cars['X']
    total_moves = 0
    target_col = board.size

    # Check any direct blocking cars in the path of X
    for col in range(x_car.col + x_car.length - 1, target_col):
        blocking_car = board.board[x_car.row - 1][col]
        if blocking_car != '_':
            if blocking_car.orientation == "H":
                moves_left = blocking_car.col - 1
                moves_right = board.size - (blocking_car.col + blocking_car.length - 1)
                total_moves += min(moves_left, moves_right)
            elif blocking_car.orientation == "V":
                moves_up = blocking_car.row - 1
                moves_down = board.size - (blocking_car.row + blocking_car.length - 1)
                total_moves += min(moves_up, moves_down)

    # Roughly account for other cars that might indirectly block the path
    for car in board.cars.values():
        if car.car == 'X':
            continue
        if car.orientation == "H" and car.row == x_car.row:
            moves_left = car.col - 1
            moves_right = board.size - (car.col + car.length - 1)
            total_moves += min(moves_left, moves_right)
        elif car.orientation == "V" and x_car.col <= car.col <= target_col:
            moves_up = car.row - 1
            moves_down = board.size - (car.row + car.length - 1)
            total_moves += min(moves_up, moves_down)

    return total_moves

def tiered_blocking_heuristic(board):
    """
    Heuristic function that calculates the cost based on:
    1. First-tier blocking cars: cars directly blocking X car's path.
    2. Second-tier blocking cars: cars blocking those cars.
    """
    x_car = board.cars['X']
    first_tier_blocks = 0
    second_tier_blocks = 0
    exit_col = board.size

    # Identify first-tier blocking cars
    for col in range(x_car.col + x_car.length - 1, exit_col):
        blocking_car = board.board[x_car.row - 1][col]
        if blocking_car != '_':
            first_tier_blocks += 1
            # Check whether the blocking car is itself blocked
            blocking_obj = board.cars[blocking_car.car]
            if blocking_obj.orientation == "H":
                # Check left
                if (blocking_obj.col > 1 and 
                    board.board[blocking_obj.row - 1][blocking_obj.col - 2] != '_'):
                    second_tier_blocks += 1
                # Check right
                right_index = blocking_obj.col + blocking_obj.length - 1
                if (right_index < board.size and
                    board.board[blocking_obj.row - 1][right_index] != '_'):
                    second_tier_blocks += 1
            else:  # orientation == "V"
                # Check up
                if (blocking_obj.row > 1 and
                    board.board[blocking_obj.row - 2][blocking_obj.col - 1] != '_'):
                    second_tier_blocks += 1
                # Check down
                down_index = blocking_obj.row + blocking_obj.length - 1
                if (down_index < board.size and
                    board.board[down_index][blocking_obj.col - 1] != '_'):
                    second_tier_blocks += 1

    # Weigh them differently
    first_tier_weight = 5
    second_tier_weight = 2

    return first_tier_blocks * first_tier_weight + second_tier_blocks * second_tier_weight

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

if __name__ == "__main__":
 
    from rushhour.classes.board import Board

    # For example, load a 6x6 puzzle from a CSV:
    data = Data()
    size = 9
    board_file = "../../gameboards/Rushhour9x9_5.csv"  # or "Rushhour6x6_1.csv", etc.
    board = Board(board_file, size, data)

    A_Star(board)
