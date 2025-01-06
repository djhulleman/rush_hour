def load(file):
    with open(file, "r") as file:
        for line in file:
            print(line)

if __name__ == "__main__":
    load('gameboards/Rushhour6x6_1.csv')