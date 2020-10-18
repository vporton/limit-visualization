#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return pow(2, -10 * x**2) + x**3

min_x = -1.0
max_x = 1.0
x_point = 0.5
width = 0.2

x = np.arange(min_x, max_x, 0.01)
y = f(x)

x2 = np.arange(x_point-0.1, x_point+0.1, 0.01)
y2 = f(x2)

figsize = (10, 5)
cols = 3
rows = 2

graph_color = 'blue'

axs = plt.figure(figsize=figsize, constrained_layout=True).subplots(rows, cols)
axs[0][0].plot(x, y, color=graph_color)
axs[0][0].set_title("Take an arbitrary function")

axs[0][1].plot(x, y, alpha=0)
axs[0][1].plot(x2, y2, color=graph_color)
axs[0][1].set_title("Its infinitely small fragment")

axs[0][2].plot(x, y, alpha=0)
axs[0][2].fill_between(x2, y2-width/2, y2+width/2, color=graph_color)
axs[0][2].set_title("Topological transformation\nto have infinitely small width")

axs[1][0].plot(x, y, alpha=0)
axs[1][0].fill_between(x2, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
axs[1][0].set_title("...does not differ of")

axs[1][1].plot(x, y, alpha=0)
for i in range(6):
    axs[1][1].fill_between(x2 + (i-4)*0.3, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
axs[1][1].set_title("Shift to infinitely many x positions")

axs[1][2].plot(x, y, alpha=0)
for i in range(6):
    axs[1][2].fill_between(x2 + (i-4)*0.3, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
axs[1][2].plot(x, [f(x_point) for t in x], color='red')
axs[1][2].set_title("Its y limit point")

plt.show()