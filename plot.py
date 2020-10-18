#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig2 = plt.figure()

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

graph_color = 'blue'

def make_frame(label):
    # ax = plt.axes(xlim=(-1, 4), ylim=(-2, 2), label=label)
    ax = plt.axes(label=label)
    ax.plot(x, y, alpha=0)
    return ax

ims = []

ax = make_frame("Take an arbitrary function")
ax.plot(x, y, color=graph_color)
ax.set_title("Take an arbitrary function")
ims.append((ax,))

ax = make_frame("Its infinitely small fragment")
ax.plot(x, y, alpha=0)
ax.plot(x2, y2, color=graph_color)
ax.set_title("Its infinitely small fragment")
ims.append((ax,))

ax = make_frame("Topological transformation\nto have infinitely small width")
ax.plot(x, y, alpha=0)
ax.fill_between(x2, y2-width/2, y2+width/2, color=graph_color)
ax.set_title("Topological transformation\nto have infinitely small width")
ims.append((ax,))

ax = make_frame("...does not differ of")
ax.plot(x, y, alpha=0)
ax.fill_between(x2, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
ax.set_title("...does not differ of")
ims.append((ax,))

ax = make_frame("Shift to infinitely many x positions")
ax.plot(x, y, alpha=0)
for i in range(6):
    ax.fill_between(x2 + (i-4)*0.3, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
ax.set_title("Shift to infinitely many x positions")
ims.append((ax,))

ax = make_frame("Its y limit point")
ax.plot(x, y, alpha=0)
for i in range(6):
    ax.fill_between(x2 + (i-4)*0.3, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
ax.plot(x, [f(x_point) for t in x], color='red')
ax.set_title("Its y limit point")
ims.append((ax,))

ani = animation.ArtistAnimation(fig2, ims, interval=1000, repeat_delay=0, blit=True)

# ani.save('plot.mp4', metadata={'artist':'Victor Porton'})
# writer = animation.FFMpegWriter(
#     fps=15, metadata={'artist':'Victor Porton'}, bitrate=1800)
ani.save("plot.gif", writer="imagemagick")

# plt.show()
