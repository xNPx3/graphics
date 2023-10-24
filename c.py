import math
import os
import time
import numpy as np

(WIDTH, HEIGHT) = os.get_terminal_size()

pi = np.pi
sin = np.sin
cos = np.cos

deg = (pi / 180)
# light = ".,-~:;=!*#$@"
light = "░▒▓█"

out = np.full((HEIGHT, WIDTH), ' ')
zbfr = np.zeros((HEIGHT, WIDTH))
points = np.mat([0, 0, 0])

plot_scale = [1, 0.5]
camera_pos = [0, 0]

np.seterr(divide='ignore', invalid='ignore')


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


def plot(data):
    col = row = -1

    zvalues = data[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)
    # z_norm = (zvalues-np.min(zvalues))/(np.max(zvalues)-np.min(zvalues))

    for p in data:
        (x, y, z) = p.T
        # center of screen, offset by scaled pos and camera pos
        col = round(WIDTH / 2 + x.item() * plot_scale[0] - camera_pos[0] - 1)
        row = round(HEIGHT / 2 - y.item() * plot_scale[1] + camera_pos[1] - 1)

        if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
            z_norm = ((-z - zmin) / (zmax - zmin)).item()
            if z_norm > zbfr[row][col]:
                # TODO: light source position
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


def translate(x, y, z):
    return np.mat([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, z]
    ])


def hollowCube(s):
    v = s // 2
    for u in range(-v, v, 1):
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


def hollowCube2(s):
    v = s // 2
    obj = np.array([[v, v, v]])

    for u in range(-v, v, 1):
        obj = np.concatenate((obj, np.mat([
            [u, v, v],
            [u, -v, v],
            [u, v, -v],
            [u, -v, -v],
            [v, u, v],
            [-v, u, v],
            [v, u, -v],
            [-v, u, -v],
            [v, v, u],
            [-v, v, u],
            [v, -v, u],
            [-v, -v, u],
        ])))

    return obj


def filledCube(s):
    w = s // 2
    for u in range(-w, w, 1):
        for v in range(-w, w, 1):
            addPoint(u, v, w)
            addPoint(u, w, v)
            addPoint(w, u, v)

            addPoint(u, v, -w)
            addPoint(u, -w, v)
            addPoint(-w, u, v)


if __name__ == "__main__":
    print(WIDTH, HEIGHT)

    hcube = hollowCube2(30)
    hcube = hcube @ RY(60 * deg) @ RX(45 * deg)

    plot(hcube)

    hcube2 = hollowCube2(10)
    hcube2 = hcube2 @ RY(-20 * deg) @ RX(20 * deg)
    plot(hcube2)

    draw()
    time.sleep(2)

    hcube2 = hcube2 @ translate(2, 1, 0)
    plot(hcube2)
    draw()


"""
    for i in range(2 * 360):
        points = points @ RY(1 * deg) @ RZ(1 * deg)
        plot(points)
        draw()
        time.sleep(0.05)
"""
