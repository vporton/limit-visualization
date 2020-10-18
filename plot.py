#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return pow(2, -10 * x**2) + x**3

min_x = -1.0
max_x = 1.0

x = np.arange(min_x, max_x, 0.01)
y = f(x)

x2 = np.arange(-0.1, 0.1, 0.01)
y2 = f(x2)

figsize = (10, 8)
cols = 3
rows = 4

axs = plt.figure(figsize=figsize, constrained_layout=True).subplots(rows, cols)
axs[0][0].plot(x, y, color='blue')
axs[0][1].plot(x, y, alpha=0)
axs[0][1].plot(x2, y2, color='blue')
axs[0][2].plot(x, y, alpha=0)
axs[0][2].fill_between(x2, y2-0.1, y2+0.1, color='blue')


# axs.show()
plt.show()