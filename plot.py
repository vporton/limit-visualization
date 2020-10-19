#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

fig = plt.figure()

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
    ax = plt.axes(label=label)
    ax.set_title(label)
    ax.plot(x, y, alpha=0)
    return ax

fileCounter = 0

def fileName():
    global fileCounter
    result = "frame{}.png".format(fileCounter)
    fileCounter += 1
    return result

ims = []

ax = make_frame("Take an arbitrary function")
ax.plot(x, y, color=graph_color)
plt.savefig(fileName())

ax = make_frame("Its infinitely small fragment")
ax.plot(x, y, alpha=0)
ax.plot(x2, y2, color=graph_color)
plt.savefig(fileName())

ax = make_frame("Topological transformation\nto have infinitely small width")
ax.plot(x, y, alpha=0)
ax.fill_between(x2, y2-width/2, y2+width/2, color=graph_color)
plt.savefig(fileName())

ax = make_frame("...does not differ of")
ax.plot(x, y, alpha=0)
ax.fill_between(x2, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
plt.savefig(fileName())

ax = make_frame("Shift to infinitely many x positions.\nThis set is the generalized limit")
ax.plot(x, y, alpha=0)
for i in range(6):
    ax.fill_between(x2 + (i-4)*0.3, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
plt.savefig(fileName())

ax = make_frame("Its y limit point is the customary limit")
ax.plot(x, y, alpha=0)
for i in range(6):
    ax.fill_between(x2 + (i-4)*0.3, [f(x_point)-width/2 for t in x2], [f(x_point)+width/2 for t in x2], color=graph_color)
ax.plot(x, [f(x_point) for t in x], color='red')
plt.savefig(fileName())

if os.system("convert -delay 200 -loop 0 frame*.png plot.gif"):
    raise "Cannot execute `convert`."

if os.system("rm -f frame*.png"):
    raise "Cannot remove temp files."
