import math
import os
import time
import numpy as np

(WIDTH, HEIGHT) = os.get_terminal_size()

pi = np.pi
sin = np.sin
cos = np.cos

deg = (pi / 180)
#light = ".,-~:;=!*#$@"
light = "░▒▓█"

out = np.full((HEIGHT, WIDTH), ' ')
zbfr = np.zeros((HEIGHT, WIDTH))
points = np.mat([0, 0, 0])

plot_scale = [1, 0.5]
camera_pos = [0, 0]


def clear():
    global points, out, zbfr

    #points = np.mat([0, 0, 0])
    out = np.full((HEIGHT, WIDTH), ' ')
    zbfr = np.zeros((HEIGHT, WIDTH))


def addPoint(x, y, z):
    global points
    p = np.array([x, y, z])
    points = np.vstack([points, p])

# ······
"""
if out[row][col] != ' ':
    if light.index(out[row][col]) < i:
        out[row][col] = char
        else:
"""

def plot():
    col = row = -1

    zvalues = points[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)
    # z_norm = (zvalues-np.min(zvalues))/(np.max(zvalues)-np.min(zvalues))

    for p in points:
        (x, y, z) = p.T
        # center of screen, offset by scaled pos and camera pos
        col = round(WIDTH / 2 + x.item() * plot_scale[0] - camera_pos[0] - 1)
        row = round(HEIGHT / 2 - y.item() * plot_scale[1] + camera_pos[1] - 1)

        if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
            z_norm = ((-z - zmin) / (zmax - zmin)).item()
            if z_norm > zbfr[row][col]:
                
                i = round(z_norm * (len(light) - 1))
                char = light[i]
            
                out[row][col] = char
                zbfr[row][col] = z_norm


def draw():
    os.system('cls')

    for row in range(HEIGHT):
        for col in range(WIDTH):
            print(out[row][col], end='')
        print()
    #print('\r', end='')

    clear()


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
    v = s // 2
    for u in range(-s // 2, s // 2, 1):
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

def filledCube(s):
    w = s // 2
    for u in range(-s // 2, s // 2, 1):
        for v in range(-s // 2, s // 2, 1):
            addPoint(u, v, w)
            addPoint(u, w, v)
            addPoint(w, u, v)

            addPoint(u, v, -w)
            addPoint(u, -w, v)
            addPoint(-w, u, v)


if __name__ == "__main__":
    print(WIDTH, HEIGHT)
    #points = np.dot(points, RY(60 * deg))
    #points = np.dot(points, RX(45 * deg))

    hollowCube(40)
    
    points = np.dot(points, RY(60 * deg))
    points = np.dot(points, RX(45 * deg))

    plot()
    draw()

    time.sleep(2)

    for i in range(2 * 360):
        points = points @ RY(1 * deg) @ RZ(1 * deg)
        plot()
        draw()
        time.sleep(0.05)
