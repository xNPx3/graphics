import math
import os
import time
import numpy as np
from numpy.linalg import multi_dot
from rotations import X, Y, Z, Axis

(WIDTH, HEIGHT) = os.get_terminal_size()

pi = np.pi
sin = np.sin
cos = np.cos

deg = (pi / 180)
# light = ".,-~:;=!*#$@"
light = "░▒▓█"

draws = 0

out = np.full((HEIGHT, WIDTH), ' ')
zbfr = np.zeros((HEIGHT, WIDTH))
points = np.mat([0, 0, 0])

plot_scale = [1, 0.5]
camera_pos = [0, 0, 0]
plane = [0, 0, 1]

np.seterr(divide='ignore', invalid='ignore')


def clearBuffers():
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

# https://paroj.github.io/gltut/Positioning/Tut04%20Perspective%20Projection.html


def plotfunc_p1(p, data):
    col = row = -1
    (x_cam, y_cam, z_cam) = camera_pos
    (px, py, pz) = p.T

    R = np.dot(p, (z_cam - plane[2]) / (z_cam - pz).item())
    (x, y, z) = R.T

    N = 1  # zNear
    F = 10  # zFar
    Z_clip = (z.item() * (N + F)) / (N - F) + (2 * N * F) / (N - F)

    zvalues = data[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)
    C = 20

    # center of screen, offset by scaled pos and camera pos
    col = round(WIDTH / 2 + x.item() * C * plot_scale[0] - camera_pos[0] - 1)
    row = round(HEIGHT / 2 - y.item() * C * plot_scale[1] + camera_pos[1] - 1)

    if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
        z_norm = ((pz.item() - zmin) / (zmax - zmin))

        # out[row][col] = '#'
        if z_norm >= zbfr[row][col]:
            # TODO: light source position
            i = round(z_norm * (len(light) - 1))
            char = light[i]

            out[row][col] = char
            zbfr[row][col] = z_norm


def plotfunc_p2(p, data):
    col = row = -1
    (x_cam, y_cam, z_cam) = camera_pos
    (px, py, pz) = p.T

    # calculate ???

    c_x = (px.item() * (plane[2] - z_cam)) / pz.item()
    c_y = (py.item() * (plane[2] - z_cam)) / pz.item()
    c_z = plane[2] - z_cam
    #print(pr_x, pr_y)

    zvalues = data[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)

    A = 1
    B = [30, 30]

    # center of screen, offset by scaled pos and camera pos
    col = round(WIDTH / 2 + c_x * A * B[0] * plot_scale[0] - camera_pos[0] - 1)
    row = round(HEIGHT / 2 - c_y * A * B[1]
                * plot_scale[1] + camera_pos[1] - 1)

    if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
        z_norm = ((pz.item() - zmin) / (zmax - zmin))

        # out[row][col] = '#'
        if z_norm >= zbfr[row][col]:
            # TODO: light source position
            lum = (len(light) - 1)
            i = round(z_norm * lum)
            char = light[i]

            out[row][col] = char
            zbfr[row][col] = z_norm


def plotfunc_p3(p, data):
    col = row = -1
    (x_cam, y_cam, z_cam) = camera_pos
    (px, py, pz) = p.T

    P = np.append(np.array(p), [1])
    #print(P)

    F = 100
    N = 0.1

    FOV = 90

    S = 1 / (np.tan((FOV / 2) * (pi / 180)))

    tr = np.mat([
        [S, 0, 0, 0],
        [0, S, 0, 0],
        [0, 0, - F / (F - N), -1],
        [0, 0, -(F * N) / (F - N), 0]
    ])

    PR = np.dot(P, tr)
    PR = np.divide(PR, np.array(PR)[0][3])
    print(PR)


def plotfunc(p, data):
    col = row = -1

    zvalues = data[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)

    (x, y, z) = p.T
    # center of screen, offset by scaled pos and camera pos
    col = round(WIDTH / 2 + x.item() * plot_scale[0] - camera_pos[0] - 1)
    row = round(HEIGHT / 2 - y.item() * plot_scale[1] + camera_pos[1] - 1)

    if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
        z_norm = ((z.item() - zmin) / (zmax - zmin))
        #print(zmin, zmax, z_norm, end=' | ')
        if z_norm >= zbfr[row][col]:
            # TODO: light source position
            i = round(z_norm * (len(light) - 1))
            char = light[i]

            out[row][col] = char
            zbfr[row][col] = z_norm


def plot(data):
    #print(type(data), data)
    np.apply_along_axis(plotfunc_p3, 1, data, data)


def old_draw(clear=True):
    os.system('cls')

    for row in range(HEIGHT):
        for col in range(WIDTH):
            print(out[row][col], end='')
        print()

    if clear:
        clearBuffers()


def draw():
    print(' | debug')
    for row in range(HEIGHT - 2):  # dont print last row to prevent jittering
        for col in range(WIDTH):
            print(out[row][col], end='')
        print()

    clearBuffers()
    # cursor to home position (top left)
    print(f'\033[H', end='')


def hollowCube(s):
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
    obj = np.array([[w, w, w]])

    for u in range(-w, w, 1):
        for v in range(-w, w, 1):
            obj = np.concatenate((obj, np.mat([
                [u, v, w],
                [u, w, v],
                [w, u, v],

                [u, v, -w],
                [u, -w, v],
                [-w, u, v],
            ])))

    return obj


def translate(data, delta):
    def _translate(p, d: np.array):
        return np.sum([p, np.array(d)], axis=0)
    return np.apply_along_axis(_translate, 1, data, delta)


if __name__ == "__main__":
    print(WIDTH, HEIGHT)
    os.system('cls')

    c1 = hollowCube(30)

    v = np.sqrt(3) / 3
    rot1 = np.array([-v, -v, -v])
    c1 = translate(c1, [20, -10, 45])
    plot(c1)
    draw()
    """
    c1 = translate(c1, [0, 0, 30])
    while True:
        c1 = multi_dot([c1, Y(1 * deg)])
        plot(c1)
        draw()
"""
