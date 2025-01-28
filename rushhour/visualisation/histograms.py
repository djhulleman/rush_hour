import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Load the data from a file
# Assuming the file is a CSV with a column named "values"
file_path = 'baseline/game7.csv'
data = pd.read_csv(file_path)

# Step 2: Create a histogram
#plt.hist(data, bins=50, color='blue', edgecolor='black')
plt.figure(figsize=(8, 6))  # Set the figure size
#box = plt.boxplot(data, patch_artist=True, boxprops=dict(facecolor='lightblue', color='blue'),
#                  medianprops=dict(color='red', linewidth=2), whiskerprops=dict(color='blue'),
#                 capprops=dict(color='blue'), flierprops=dict(marker='o', color='darkorange', alpha=0.7))
plt.hist(data, bins=50)

# Add grid for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)


# Step 3: Customize the plot        
plt.title('Boxplot of 12x12 game 7')
plt.ylabel('Steps')
plt.xticks([1], ["Dataset"]) 

# Step 4: Show the plot
plt.show()