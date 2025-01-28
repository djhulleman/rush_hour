import pandas as pd
import matplotlib.pyplot as plt

# Replace 'file_path.csv' with your actual file name
data = pd.read_csv("solutions/Hillclimber/cleaned_results.csv")
print(data.head())  # Display the first few rows to inspect data structure

# Clean up columns by dropping "Unnamed" columns
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]


# Line plots for all steps series
plt.figure(figsize=(12, 6))

# Plot each 'steps' column
for col in data.columns:
    plt.plot(data.index, data[col], label=col)

plt.title("Hillclimbers 12x12")
plt.xlabel("Time")
plt.ylabel("Solution steps")
plt.legend()
plt.grid(True)
plt.show()