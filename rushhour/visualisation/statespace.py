import numpy as np
import math
import csv

def load_board(filename, size):
    # Initialize separate lists for cars and trucks
    cars = [0] * (2 * size)
    trucks = [0] * (2 * size)
    
    with open(filename, mode='r') as file:
        csvFile = csv.reader(file)
        next(csvFile)  # skip the first header line

        for lines in csvFile:
            name, orientation, col, row, length = lines[0], lines[1], int(lines[2]), int(lines[3]), int(lines[4])
            if orientation == "H":
                if length == 2:
                    cars[row-1] += 1
                if length == 3:
                    trucks[row-1] += 1                    
            if orientation == "V":
                if length == 2:
                    cars[col + size - 1] += 1
                if length == 3:
                    trucks[col + size - 1] += 1
    return (cars, trucks)

def binomial(n, k):
    return math.comb(n, k) if k <= n else 0

def factorial(n):
    return math.factorial(n)

def row_permutations(size, cars, trucks):
    b = 2*cars + 3*trucks
    v = size - b
    if v == size:
        return 1
    S = binomial(v + cars + trucks, cars + trucks)
    P = factorial(cars + trucks)/(factorial(cars)*factorial(trucks))
    return S*P

# Functie om de statespace te berekenen
def calculate_statespace(board, size):
    cars, trucks = load_board(board, size)  # Load the board and get car/truck counts
    row_states = []  # Store state-space for each row and column
    
    for i in range(2 * size):
        a = cars[i]      # Cars in the row/column
        t = trucks[i]    # Trucks in the row/column
        row_states.append(row_permutations(size, a, t))  # Calculate permutations for this row/column
    
    print("Row/Column States:", row_states)
    print("Total Statespace:", np.prod(row_states))  


# Voorbeeld gebruik
if __name__ == '__main__':
    # Inladen van het bordbestand
    calculate_statespace("gameboards/Rushhour6x6_1.csv", 6)