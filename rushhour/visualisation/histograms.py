import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Load the data from a file
# Assuming the file is a CSV with a column named "values"
file_path = 'baseline/rendom_output_7.csv'
data = pd.read_csv(file_path)

# Step 2: Create a histogram
plt.hist(data, bins=30, color='blue', edgecolor='black')

# Step 3: Customize the plot
plt.title('Histogram of Values')
plt.xlabel('Value Range')
plt.ylabel('Frequency')

# Step 4: Show the plot
plt.show()