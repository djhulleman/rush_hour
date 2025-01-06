def print_board(n, car):
    for i in range(0, n):
        for j in range(0, n):
            print('_', end=" ")
        print()

if __name__ == "__main__":
    print_board(8)