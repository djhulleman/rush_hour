from game import *
from data import *

# select board size and game
size = 9
game = 5

# Create data process 
data = Data()

# create game board
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size, data)

amount = []

while len(amount) < 100:
    solve(board)
    data.export_moves()
    file_name = "output.csv" 
    with open(file_name, 'r') as file:
        # Read all lines and count them
        line_count = sum(1 for line in file) - 1
    amount.append([line_count])
    
new_file = "output_sum.csv"  
with open(new_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(amount)