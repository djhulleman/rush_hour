import copy

def IDS(board):
    max_depth = 0
    while True:
        # Perform DFS with the current depth limit
        result = DFS_Limited(board, max_depth)
        if result is not None:
            return result  # Goal found at this depth
        max_depth += 1  # Increase depth limit for the next iteration

def DFS_Limited(board, depth_limit):
    if board.check_finish():  # Check if the goal state is reached
        return board  # Goal found, return the current board state
    if depth_limit == 0:
        return None  # Reached maximum depth, no solution found at this level
    
    # Generate all children of the current board state
    for child in generate_children(board):
        result = DFS_Limited(child, depth_limit - 1)
        if result is not None:
            return result  # Return the result if a solution is found
    
    return None  # No solution found at this level

def generate_children(board):
    children = []  # List to store child states
    for car in board.cars.values():  # Loop through each car in the current board state
        if car.orientation == "H":  # Horizontal car
            if board.check_move(car.car, 1):  # Check if move left is possible
                child_board = copy.deepcopy(board)  # Deep copy to avoid side effects
                child_board.move(car.car, 1)  # Move the car left in the child state
                children.append(child_board)  # Add the new state to children
                
            if board.check_move(car.car, 2):  # Check if move right is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2)  # Move the car right in the child state
                children.append(child_board)
        
        elif car.orientation == "V":  # Vertical car
            if board.check_move(car.car, 1):  # Check if move up is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 1)  # Move the car up in the child state
                children.append(child_board)
                
            if board.check_move(car.car, 2):  # Check if move down is possible
                child_board = copy.deepcopy(board)
                child_board.move(car.car, 2)  # Move the car down in the child state
                children.append(child_board)
    
    return children
