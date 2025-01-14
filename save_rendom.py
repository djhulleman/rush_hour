from game import *
import csv
from rushhour.classes.data import Data
from rushhour.classes.board import Board

# select board size and game
size = 6
game = 3

# Create data process 
data = Data()

# create game board
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

amount = []

while len(amount) < 20000:
    solve(board)
    data.export_moves()
    line_count = 0
    file_name = "output.csv" 
    with open(file_name, 'r') as file:
        # Read all lines and count them
        line_count = sum(1 for line in file) - 1
    amount.append([line_count])
    
new_file = "rendom_output_test.csv"  
with open(new_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(amount)