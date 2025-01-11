import csv

class Data:
    '''create a data opject that
    will save the staps made'''
    def __init__(self):
        self.output_data = [
            ["car", "move"]
        ]
    def save_move(self, car, direction):
        '''store steps'''   
        car_name = car.car

        if direction == 1:
            self.output_data.append([car_name, "-1"])
        elif direction == 2:
            self.output_data.append([car_name, "1"])
        else:
            self.output_data.append("Fout")
    
    def export_moves(self):
        '''makes file that has all the steps in them'''
        # create file
        file_name = "output.csv"
        # open the creades file and put the steps in
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.output_data)

        print(f"Data is geexporteerd in {file_name}")

