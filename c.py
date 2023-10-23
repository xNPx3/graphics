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

plot_scale = [1, 0.5]
camera_pos = [0, 0]


def addPoint(x, y, z):
    points.append(np.array([x,y,z]))


def plot():
    col = row = -1

    for p in points:
        (x, y, z) = p
        # center of screen, offset by scaled pos and camera pos
        col = round(WIDTH / 2 + x * plot_scale[0] - camera_pos[0] - 1)
        row = round(HEIGHT / 2 - y * plot_scale[1] + camera_pos[1] - 1)

        if((0 <= col < WIDTH) and (0 <= row < HEIGHT)):
            out[row][col] = '#'


def draw():
    # os.system('cls')

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


def hollowCube(s):
    for u in range(-s // 2, s // 2, 1):
        v = s // 2

        addPoint(u, v, v)
        addPoint(u, -v, v)
        addPoint(u, v, -v)
        addPoint(u, -v, -v)

        addPoint(v, u, v)
        addPoint(-v, u, v)
        addPoint(v, u, -v)
        addPoint(-v, u, -v)

        addPoint(v, v, u)
        addPoint(-v, v, u)
        addPoint(v, -v, u)
        addPoint(-v, -v, u)


if __name__ == "__main__":  # ······
    print(WIDTH, HEIGHT)

    hollowCube(30)

    #points = np.dot(points, RZ(pi / 4))
    
    plot()
    draw()
