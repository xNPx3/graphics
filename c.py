import math
import os
import time
import numpy as np


(WIDTH, HEIGHT) = os.get_terminal_size()

pi = np.pi
sin = np.sin
cos = np.cos

out = np.full((HEIGHT, WIDTH), ' ')
points = []


def scale(x, out_range=(0, 1), axis=None):
    domain = np.min(x, axis), np.max(x, axis)
    y = (x - (domain[1] + domain[0]) / 2) / (domain[1] - domain[0])
    return y * (out_range[1] - out_range[0]) + (out_range[1] + out_range[0]) / 2


def plot():
    col = row = -1

    for (x, y, z) in points:
        col = round(WIDTH / 2 + x * 2.3 - 1)
        row = round(HEIGHT / 2 - y - 1)

        if((0 <= col < WIDTH) and (0 <= row < HEIGHT)):
            out[row][col] = '·'


def draw():
    #os.system('cls')

    for row in range(HEIGHT):
        for col in range(WIDTH):
            print(out[row][col], end='')
        print()


# rotation matrices
def RX(a):
    return np.mat([
        [1, 0, 0],
        [0, cos(a), -sin(a)],
        [0, sin(a), cos(a)]
    ])


def RY(a):
    return np.mat([
        [cos(a), 0, sin(a)],
        [0, 1, 0],
        [-sin(a), 0, cos(a)]
    ])


def RZ(a):
    return np.mat([
        [cos(a), -sin(a), 0],
        [sin(a), cos(a), 0],
        [0, 0, 1]
    ])


if __name__ == "__main__": #······
    print(WIDTH, HEIGHT)

    points += [[0, 0, 0]]
    points += [[20, 2, 3]]
    points += [[-7, 6, 0]]
    print(points)

    plot()
    draw()
