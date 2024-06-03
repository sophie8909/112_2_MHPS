import matplotlib.pyplot as plt
import pandas as pd

# Read the data from the file
filename = './experient_1_result.txt'
data = pd.read_csv(filename, sep=' ', header=None, names=['col1', 'col2', 'col3', 'col4'])

# Plotting
plt.figure(figsize=(10, 6))

# Plot all points with default color
plt.scatter(data['col4'], data['col2'], color='blue')

# Highlight specific points in red
highlight_indices = [0]  # Python uses 0-based indexing
plt.scatter(data.loc[highlight_indices, 'col4'], data.loc[highlight_indices, 'col2'], color='red')

plt.xlabel('fitness')
plt.ylabel('lineNum')
plt.title('nsga-ii result')
plt.grid(True)
plt.show()