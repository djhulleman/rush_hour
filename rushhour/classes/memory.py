class Memory:
    """
    Memory class for saving, hasing and comparing board states
    """

    def __init__(self):
        """
        Contains a list and dict with board states
        """
        # List with actual board states
        self.saved_boards = []
        # Dict with hasehd board states for fast comparison
        self.board_hashes = {}

    def hash_board(self, board_copy, car_names):
        """
        The function returns the hash of a cetain board state
        Creates a list of car properties in a certain board state.
        This list is hashed into string notation. 
        """
        # list for car properties of a given board state
        cars_properties = []

        # append properties to the list
        for key in car_names:
            r, c = board_copy[key]
            cars_properties.append(f"{key}:{r}:{c}")

        # return a hashed version of this board state
        return "|".join(cars_properties)
        
    def save_board(self, cars, car_names):
        """
        Saves the current board state in self.saved_boards and its hash in self.board_hashes.
        """
        # Create a dictionary to store the positions of all cars on the board.
        # The key is the car's name, and the value is a tuple (row, column) indicating its position.
        board_copy = {}

        # iterate over all cars to extract their positions and create a board_copy.
        for key, car in cars.items():
            board_copy[key] = (car.row, car.col)
        
         # save the current board state in the list of saved boards.
        self.saved_boards.append(board_copy)

        # generate a unique hash for the current board state.
        # use the hash to record the board's position in the saved_boards list.
        h = self.hash_board(board_copy, car_names)
        self.board_hashes[h] = len(self.saved_boards) - 1 # the hash is the key; the value is the board's index in saved_boards.

    def compare_boards(self, cars, car_names):
        """
        Compares a current board state with previously saved boards.
        """
        # create a dictionary to represent the current board state. 
        current_board_copy = {}

        # iterate over all cars to extract their positions and create a board_copy.
        for key, car in cars.items():
            if isinstance(car, tuple):
                # If `cars` contains tuples
                current_board_copy[key] = car
            else:
                # If `cars` contains `Car` objects
                current_board_copy[key] = (car.row, car.col)

        # generate a hash for the current board state.
        h = self.hash_board(current_board_copy, car_names)

        # return the index of the matching board from saved_boards, if it exists. Else, return None
        return self.board_hashes.get(h, None)
    
    def del_hashes(self, memory, n, car_names):
        """
        Deletes board hashes beyond a specified index (n) from self.board_hashes.
        """
        # get the list of boards to remove from saved_boards starting from index n+1.
        boards_to_remove = memory.saved_boards[n+1:] 

        # iterate over the boards to remove and delete their hashes from board_hashes.
        for boardt in boards_to_remove:
            # generate the hash for each board state.
            h = memory.hash_board(boardt, car_names)
            # remove the hash from board_hashes, if it exists.
            memory.board_hashes.pop(h, None)

    def create_board(self, board, size, position):
        """
         Recreates a board from a saved state.
        """

        # initialize an empty NxN board with underscores.
        board.board = [['_'] * size for _ in range(size)]

        # Get car properties from saved_boards list 
        saved_board = self.saved_boards[position]

        # Update each car’s row and col 
        for car_name, (r, c) in saved_board.items():
            board.cars[car_name].row = r
            board.cars[car_name].col = c

        # Place the cars on the 2D matrix
        for car in board.cars.values():
            if car.orientation == "H":
                for j in range(car.length):
                    board.board[car.row - 1][car.col + j - 1] = car
            else:  # orientation == "V"
                for j in range(car.length):
                    board.board[car.row + j - 1][car.col - 1] = car