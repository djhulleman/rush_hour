import csv

class Data:
    '''create a data opject that
    will save the staps made'''
    def __init__(self):
        self.output_data = [
            ["car", "move"]
        ]

    def save_move(self, car, direction):
        '''Store steps when given car object or name and direction'''
        # handle both car object and car name
        car_name = car.car if hasattr(car, 'car') else car

        if direction == 1:
            self.output_data.append([car_name, "-1"])
        elif direction == 2:
            self.output_data.append([car_name, "1"])
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
        if direction == "-1":
            self.output_data.append([car_name, "-1"])
        elif direction == "1":
            self.output_data.append([car_name, "1"])
        else:
            print(f"auto {car_name}, richting {direction}")
            self.output_data.append(["Fout"])
            