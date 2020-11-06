#!/usr/bin/env python3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

fig = plt.figure()

min_x = -1.0
max_x = 1.0
x_point = 0.4
width = 0.2

def f1(x):
    return pow(2, -10 * x**2) + x**3

def f2(x):
    return f1(x) + 0.3

def f(x):
    return np.piecewise(x, [x < x_point, x >= x_point], [f1, f2])

x = np.arange(min_x, max_x, 0.01)
y = f(x)

x_minus = np.arange(min_x, x_point, 0.01)
y_minus = f(x_minus)
x_plus = np.arange(x_point, max_x, 0.01)
y_plus = f(x_plus)

x2 = np.arange(x_point-0.1, x_point+0.1, 0.01)
y2 = f(x2)

x2_minus = np.arange(x_point-0.1, x_point, 0.01)
x2_plus = np.arange(x_point, x_point+0.1, 0.01)
y2_minus = f(x2_minus)
y2_plus = f(x2_plus)

graph_color = 'blue'

def make_frame(label):
    ax = plt.axes(label=label)
    ax.set_title(label)
    ax.plot(x, y, alpha=0)
    return ax

def fileName(number):
    return "discontinuous{}.png".format(number)


def generate_frame0():
    ax = make_frame("Take an arbitrary function")
    ax.plot(x_minus, y_minus, color=graph_color)
    ax.plot(x_plus, y_plus, color=graph_color)
    plt.plot((x_point, x_point), (f1(x_point), f2(x_point)), linestyle='--', color='gray')
    plt.savefig(fileName(0))

def generate_frame1():
    ax = make_frame("Its infinitely small fragment")
    ax.plot(x, y, alpha=0)
    ax.plot(x2_minus, y2_minus, color=graph_color)
    ax.plot(x2_plus, y2_plus, color=graph_color)
    # plt.axline((x_point, f1(x_point)), (x_point, f2(x_point)-1), marker='o')
    plt.plot((x_point, x_point), (f1(x_point), f2(x_point)), linestyle='--', color='gray')
    plt.savefig(fileName(1))

def generate_frame2():
    ax = make_frame("Topological transformation\nto have infinitely small width")
    ax.plot(x, y, alpha=0)
    ax.fill_between(x2_minus, y2_minus-width/2, y2_minus+width/2, color=graph_color)
    ax.fill_between(x2_plus, y2_plus-width/2, y2_plus+width/2, color=graph_color)
    plt.savefig(fileName(2))

def generate_frame3():
    ax = make_frame("...does not differ of")
    ax.plot(x, y, alpha=0)
    ax.fill_between(x2_minus, [f1(x_point)-width/2 for t in x2_minus], [f1(x_point)+width/2 for t in x2_minus], color=graph_color)
    ax.fill_between(x2_plus, [f2(x_point)-width/2 for t in x2_plus], [f2(x_point)+width/2 for t in x2_plus], color=graph_color)
    plt.savefig(fileName(3))

def generate_frame4():
    ax = make_frame("Shift to infinitely many x positions.\nThis set is the generalized limit")
    ax.plot(x, y, alpha=0)
    for i in range(6):
        ax.fill_between(x2_minus + (i-4)*0.3, [f1(x_point)-width/2 for t in x2_minus], [f1(x_point)+width/2 for t in x2_minus], color=graph_color)
        ax.fill_between(x2_plus + (i-4)*0.3, [f2(x_point)-width/2 for t in x2_plus], [f2(x_point)+width/2 for t in x2_plus], color=graph_color)
        ell = matplotlib.patches.Ellipse((x_point + (i-4)*0.3, (f1(x_point)+f2(x_point)) / 2), 0.285, 0.76, fill=False, linestyle='--', linewidth=0.5)
        ax.add_artist(ell)
    plt.savefig(fileName(4))

def generate_frame(number):
    h = [generate_frame0, generate_frame1, generate_frame2, generate_frame3, generate_frame4]
    h[number]()

# if os.system("convert -delay 200 -loop 0 frame*.png plot.gif"):
#     raise "Cannot execute `convert`."

# if os.system("rm -f frame*.png"):
#     raise "Cannot remove temp files."

ids = (int(x) for x in sys.argv[1:])
for id in ids:
    generate_frame(id)
