#function IDS(initial_state, goal_state):
def IDS(board):
#    max_depth = 0  // Initial depth limit
    max_depth = 0
#    while True:
    while True:
#        result = DFS_Limited(initial_state, goal_state, max_depth)
        result = DFS_Limited(board, max_depth)
#        if result is not None:
        if result is not None:
#            return result  // Goal found at this depth
            return result
#        max_depth += 1  // Increase depth limit for the next iteration
        max_depth += 1


#function DFS_Limited(state, goal_state, depth_limit):
def DFS_Limited(board, depth_limit):
#    if state == goal_state:
    if board.check_finish:
#       return state  // Goal found, return the solution
        return board
#    if depth_limit == 0:
    if depth_limit == 0:
#        return None  // Reached maximum depth, return no solution
        return None
#    for each child_state in generate_children(state):
#        result = DFS_Limited(child_state, goal_state, depth_limit - 1)
#        if result is not None:
#            return result  // Return the result if found a solution
#    return None  // No solution found at this level


#function generate_children(state):
def generate_children(state):
#    children = []  // List to store child states
    children = []
#    for each car in state.cars:  // Loop through each car on the board
#        if car.orientation == "H":  // If the car is horizontal
#            // Check possible moves for horizontal car
#          if can_move_left(car, state):  // Check if the car can move left
#                child_state = create_new_state(state)  // Create a copy of the current state
#                move_car_left(car, child_state)  // Move the car left in the copied state
#                children.append(child_state)  // Add the new state to the children list
#            
#            if can_move_right(car, state):  // Check if the car can move right
#                child_state = create_new_state(state)  // Create a copy of the current state
#                move_car_right(car, child_state)  // Move the car right in the copied state
#                children.append(child_state)  // Add the new state to the children list

#        else if car.orientation == "V":  // If the car is vertical
#            // Check possible moves for vertical car
#            if can_move_up(car, state):  // Check if the car can move up
#                child_state = create_new_state(state)  // Create a copy of the current state
#                move_car_up(car, child_state)  // Move the car up in the copied state
#                children.append(child_state)  // Add the new state to the children list

#            if can_move_down(car, state):  // Check if the car can move down
#                child_state = create_new_state(state)  // Create a copy of the current state
#                move_car_down(car, child_state)  // Move the car down in the copied state
#                children.append(child_state)  // Add the new state to the children list

#    return children  // Return the list of child states

