import csv

class Data:
    '''create a data opject that
    will save the staps made'''
    def __init__(self):
        self.output_data = [
            ["car", "move"]
        ]

    def save_move(self, car, direction, steps=1):
        '''Store steps when given car object or name and direction'''
        # Handle both car object and car name
        car_name = car.car if hasattr(car, 'car') else car

        if direction == 1:
            self.output_data.append([car_name, -1*steps])
        elif direction == 2:
            self.output_data.append([car_name, steps])
        else:
            self.output_data.append(["Fout"])

    
    def export_moves(self, file_name = "output.csv" ):
        '''makes file that has all the steps in them'''
        # open the creades file and put the steps in
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.output_data)

        print(f"Data is geexporteerd in {file_name}")
        
    def del_moves(self, end):
        '''deleades moves'''
        del self.output_data[end+1:]
    
    def save_list_moves(self, car_name, direction):
        '''saves the move given the car name and the direction'''
        self.output_data.append([car_name, direction])
    
    def count_moves(self):
        # Start by counting the first element
        count = 0
        for i in range(1, len(self.output_data)):
            # Only count when the current item is different from the previous
            if self.output_data[i] != self.output_data[i - 1]:
                count += 1
        return count