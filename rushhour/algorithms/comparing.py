import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_with_memory import *
import time
import os

# select board size and game
size = 6
game = 3

# Create data process 
data = Data()
board_file = f'gameboards/Rushhour{size}x{size}_{game}.csv'
paths = {}

# Helper function to create a unique file name based on timestamp
def generate_unique_filename():
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    return f"output_{timestamp}.csv"

def make_dict(file_name, dict): 
    # Count the lines in the file to store it with the file name
    line_count = sum(1 for line in open(file_name))  # count lines in file
    dict[line_count] = file_name

def compare_files(path1, path2):
    '''see how much file compair and save the comapires'''
    output_path = 'overlap_output.csv'
    print(type(path1), type(path2), type(output_path))
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2, open(output_path, 'wb') as output:
        index = 0
        while True:
            byte1 = f1.read(1)
            byte2 = f2.read(1)
            # If we reach the end of one of the files or bytes differ, stop
            if byte1 != byte2 or not byte1 or not byte2:
                break
            output.write(byte1)
        return output_path



'''take random paths'''
teller = 0
while teller < 3:
    finished = random_with_memory(board_file)
    name = generate_unique_filename()
    finished.data.export_moves(name)
    line_count = 0 
    make_dict(name, paths)
    teller += 1
    print(teller)

print("one done")

'''compair rendom paths'''
# sort the keys form smallest to biggeste
sorted_keys = sorted(paths.keys())
first_smallest_key = sorted_keys[0]
second_smallest_key = sorted_keys[1]
overlap = compare_files(paths[first_smallest_key], paths[second_smallest_key])

print("two done")

'''run the compaired path'''
board = Board(board_file, size, data)
with open(overlap, mode='r') as file:
    csvFile = csv.reader(file)
    next(csvFile)
    for i, lines in enumerate(csvFile):
        direction = 0
        move = int(lines[1])
        if move == 1:
            direction = 2
        elif move == -1:
            direction = 1
        board.move(lines[0], direction)

print("three done")

def random_solve(input_board, file_name):
    '''algorithm that takes random steps to solve the puzzle'''
    # create object for car that needs to get out 
    complete = False
    n = 0
    # Prevent infinite loops
    max_iterations = 3
    while not complete and n < max_iterations:
        # chose random car and random direction
        random_car = random.choice(list(input_board.cars.keys()))  
        random_move = random.choice([1, 2])
        # move the car if possible
        input_board.move(random_car, random_move) 
        n += 1
        # check if the red car is at the end
        complete = input_board.check_finish()
    data.export_moves(file_name)



'''do random n times and save path'''
N = 0
best_path = {}
while N < 20:
    name = generate_unique_filename()
    random_solve(board,name)
    make_dict(name, best_path)
    N += 1
print("four done")

'''take the fastes path and make it the output'''
sorted_keys = sorted(best_path.keys())
smallest_key = sorted_keys[0]
old_file = best_path[smallest_key]
new_file = 'bestpath.csv'
# Check if the file exists and rename
if os.path.exists(old_file):
    os.rename(old_file, new_file)

'''deleade files'''

for file_path in best_path.values():
    if os.path.exists(file_path):
        os.remove(file_path) 
    else:
        print("no file found")
        
os.remove("overlap_output.csv")
 
