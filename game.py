import models
#import board
import csv

# Function to load cars from the CSV file
def get_cars():
    filename = 'gameboards/Rushhour6x6_1.csv'
    with open(filename, mode ='r')as file:
        for lines in file:
                print(lines)

# Entry point of the script
if __name__ == "__main__":
    get_cars()
