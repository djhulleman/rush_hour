from game import *

size = 6
game = 1

# create game board and show it
board = Board(f'gameboards/Rushhour{size}x{size}_{game}.csv', size)

solve(board)

