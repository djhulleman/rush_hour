import csv

class Data:
    '''
    creates a data opject that will handle data ouput from algorithms 
    '''

    def __init__(self):
        """
        A list of moves made by a car, in the required layout for check50
        """

        self.output_data = [
            ["car", "move"]
        ]

    def save_move(self, car, direction, steps=1):
        '''
        Stores moves when at least a car and direction in given
        '''

        # handle both car object and car name
        car_name = car.car if hasattr(car, 'car') else car

        if direction == 1:
            self.output_data.append([car_name, -1*steps])
        elif direction == 2:
            self.output_data.append([car_name, steps])
        else:
            self.output_data.append(["Fout"])

    
    def export_moves(self, file_name = "output.csv" ):
        '''
        Exports the self.output_data into a csv file with name file_name
        '''

        # create csv file for importing output data 
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.output_data)

        print(f"Data is geexporteerd in {file_name}")
        
    def del_moves(self, end):
        '''
        deleades moves from the self.output_data list
        '''

        del self.output_data[end+1:]
    
    def save_list_moves(self, car_name, direction):
        '''
        saves a move when car and direction is given.
        Is the same as save_move() but stores a move as 1 or 2 instad of 1 or -1
        '''

        self.output_data.append([car_name, direction])
    
    def count_moves(self):
        '''
        counts the unique moves in output_data by counting consecutive moves as one
        '''

        count = 0
        for i in range(1, len(self.output_data)):
            # Only count when the current item is different from the previous
            if self.output_data[i] != self.output_data[i - 1]:
                count += 1
        return count