import csv

class Data:

    def __init__(self):
        self.output_data = [
            ["move", "car"]
        ]
    def save_move(self, car, direction):    
        car_name = car.car

        if direction == 1:
            self.output_data.append([car_name, "-1"])
        elif direction == 2:
            self.output_data.append([car_name, "1"])
        else:
            self.output_data.append("Fout")
    
    def export_moves(self):
        file_name = "output.csv"
        
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.output_data)

        print(f"Data is geexporteerd in {file_name}")

