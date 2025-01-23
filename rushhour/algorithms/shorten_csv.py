import csv

def combine_moves(input_file = 'output.csv', output_file = 'output.csv'):
    """
    will shorten a csv output by combining consecutive moves of the same car.
    This makes sure the csv file displays the actual steps neccesary to solve a Rush hour game
    """

    with open(input_file, mode='r') as file:
        input_file = csv.reader(file)
        header = next(input_file)  # read the header
        
        # make sure file has 'car' and 'move' columns
        if header != ['car', 'move']:
            raise ValueError("File must have a 'car and 'move' column")
        
     
        # copy csv file exluding header in a list
        moves = []
        for row in input_file:
            car, move = row[0], int(row[1])  # Convert move to integer
            moves.append([car, move])

        combined = []
        current_car = moves[0][0]
        current_move = moves[0][1]
        n = 0

        # check for consecutives moves and add up if so, else append and move on
        for i in range(1, len(moves)):
            next_car, next_move = moves[i]
            if current_car == next_car:
                current_move += next_move
            else:
                combined.append([current_car, current_move])
                current_car = next_car
                current_move = next_move
                n += 1

        # append last car and move
        combined.append([current_car, current_move])
        n += 1

    # write the combined data to the output file
    with open(output_file, mode='w', newline='') as file:
        outputfile = csv.writer(file)
        outputfile.writerow(['car', 'move'])  # write the header
        outputfile.writerows(combined)

    print(f"Combine moves saved {output_file}")

    return n
