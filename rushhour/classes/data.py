import csv

class Data:
    '''create a data opject that
    will save the staps made'''
    def __init__(self):
        self.output_data = [
            ["car", "move"]
        ]
    def save_move(self, car, direction):
        '''store steps when given car opject and direction'''   
        car_name = car.car

        if direction == 1:
            self.output_data.append([car_name, "-1"])
        elif direction == 2:
            self.output_data.append([car_name, "1"])
        else:
            self.output_data.append("Fout")
    
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
        if direction == 1:
            self.output_data.append([car_name, "-1"])
        elif direction == 2:
            self.output_data.append([car_name, "1"])
        else:
            self.output_data.append("Fout")