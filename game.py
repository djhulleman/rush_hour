from models import *
from board import *

#import board
#cars = get_cars('gameboards/Rushhour6x6_1.csv')
#board = create_board(6)
#print(board)

#board = place_cars(board, cars)
#print(board)


board = Board('gameboards/Rushhour6x6_1.csv', 6)
board.print()