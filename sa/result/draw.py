import numpy as np
import matplotlib.pyplot as plt

f = open("100_20/1.txt", "r")
data = []
x = range(10001)

for lines in f.readlines():
    data.append(int(lines))


f.close()

plt.plot(x, data, "b")
plt.show()
