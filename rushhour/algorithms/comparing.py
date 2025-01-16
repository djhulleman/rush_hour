import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board
from rushhour.algorithms.random_with_memory import *
from itertools import combinations
import time
import os

# select board size and game
size = 6
game = 1

# Create data process 
board_file = f'gameboards/Rushhour{size}x{size}_{game}.csv'


# Helper function to create a unique file name based on timestamp
def generate_unique_filename():
    # Current timestamp in nanoseconds
    timestamp = time.time_ns()
    return f"output_{timestamp}.csv"

def make_dict(file_name, dict): 
    # Count the lines in the file to store it with the file name
    line_count = sum(1 for line in open(file_name))  # count lines in file
    dict[file_name] = line_count
        

def compare_files(path1, path2, output_name):
    '''see how much file compair and save the comapires'''
    aantal = 0
    with open(path1, 'r') as f1, open(path2, 'r') as f2, open(output_name, 'w', newline='') as output:
        while True:
            aantal += 1
            line1 = f1.readline()
            line2 = f2.readline()
            # If we reach the end of one of the files or bytes differ, stop
            if line1 != line2 or not line1 or not line2:
                break
            print(line1)
            output.write(line1) 
    return aantal

def get_board(overlap, board_overlap):
    '''make a board that has the overlapping steps'''
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
            if board_overlap.move(lines[0], direction):
                print(f"Applied move {lines[0]} with direction {direction}")
    return board_overlap


'''take random paths'''
paths = {}
teller = 0
while teller < 20:
    data = Data()
    board = Board(board_file, size, data)
    finished = random_with_memory(board)
    name = generate_unique_filename()
    finished.data.export_moves(name)
    line_count = 0 
    make_dict(name, paths)
    teller += 1

'''compair rendom paths'''
sorted_items = sorted(paths.items(), key=lambda item: item[1])
# Get the top 10 smallest items
top_10 = sorted_items[:10]
overlap_results = []
# Compare all pairs of the top 10 items
for path1, path2 in combinations(top_10, 2):
    name = generate_unique_filename()
    aantal = compare_files(path1[0], path2[0], name)
    overlap_results.append((name, aantal))
# Get the maximum overlap result
overlap_file_name = max(overlap_results, key=lambda x: x[1])[0]



'''do random n times and save path'''
N = 0
best_path = {}
while N < 10:
    name = generate_unique_filename()
    # genereer een bord met de overlap stappen,
    # sla daarna de rendom stappen erbij op
    data = Data()
    board_for_overlap = Board(board_file, size, data)
    board_overlap = get_board(overlap_file_name, board_for_overlap)
    finished = random_with_memory(board_overlap)
    name = generate_unique_filename()
    finished.data.export_moves(name)
    make_dict(name, best_path)
    N += 1

'''take the fastes path and make it the output'''
sorted_items = sorted(best_path.items(), key=lambda item: item[1])
number = sorted_items[0]
old_file = sorted_items[0][0]
new_file = 'bestpath.csv'
# Check if the file exists and rename
if os.path.exists(old_file):
    os.rename(old_file, new_file)

'''deleade files'''
# Delete files in paths except 'bestpath.csv'
for file_path in paths.keys():
    if os.path.exists(file_path) and file_path != 'bestpath.csv':
        os.remove(file_path)
    else:
        print("No file found: ", file_path)

# Delete files in best_path except 'bestpath.csv'
for file_path in best_path.keys():
    if os.path.exists(file_path) and file_path != 'bestpath.csv':
        os.remove(file_path)
    else:
        print("No file found: ", file_path)

for name, _ in overlap_results:
    # Check if this is not the file with the highest overlap
    if name != overlap_file_name:
         # Delete the file
        os.remove(name)
        print(f"Deleted file: {name}")
    else:
        print(f"Error deleting file {name}")

print(number)

