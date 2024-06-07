import matplotlib.pyplot as plt
import pandas as pd

# 讀取數據
filename = './experient_1_result.txt'
data = pd.read_csv(filename, sep=' ', header=None, names=['col1', 'col2', 'col3', 'col4'])

# 繪圖
plt.figure(figsize=(10, 6))

# 使用實心圓標記所有點
plt.scatter(data['col4'], data['col2'],facecolors='none', edgecolors='blue', marker='o')

# 使用空心圓標記特定點
highlight_indices = [0, 6, 12, 19]  # Python使用0為起始索引
plt.scatter(data.loc[highlight_indices, 'col4'], data.loc[highlight_indices, 'col2'], color='red',  marker='o')

plt.xlabel('fitness')
plt.ylabel('lineNum')
plt.title('nsga-ii result')
plt.grid(True)
plt.show()
