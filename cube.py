import math
import os
import time
import numpy as np

(WIDTH, HEIGHT) = os.get_terminal_size()
print(WIDTH, HEIGHT)

pi = math.pi
out = [[' ' for i in range(WIDTH)] for j in range(HEIGHT)]
zBuffer = [[-1111 for i in range(WIDTH)] for j in range(HEIGHT)]
clear = "\n" * HEIGHT
light = ".,-~:;=!*#$@"

counter = 0


def plot(x, y, z, char='#'):
    global out, zBuffer
    col = round(WIDTH / 2 + x * 2.3 - 1)
    row = round(HEIGHT / 2 - y - 1)

    if z == 0:
        z = 1

    ooz = 1 / z

    if((0 <= col < WIDTH) and (0 <= row < HEIGHT)):
        if z > zBuffer[row][col]:
            out[row][col] = char
            zBuffer[row][col] = z


def draw():
    global out, zBuffer
    os.system('cls')

    for row in range(HEIGHT):
        for col in range(WIDTH):
            print(out[row][col], end='')
        print()

    # rotation axis
    """gap = 2
    for x in range(-WIDTH, WIDTH ):
        plot(x * gap, 0, -20, 'x')
        for y in range(-HEIGHT, HEIGHT):
            plot(0, y * gap, -20, 'y')
            plot(x, x, -20, 'a')"""


def rotateX(x, y, z, a):
    a = a * (pi / 180)  # convert to radians
    s = math.sin(a)
    c = math.cos(a)

    _y = y * c + z * s
    _z = y * -s + z * c

    return (x, _y, _z)


def rotateY(x, y, z, a):
    a = a * (pi / 180)  # convert to radians
    s = math.sin(a)
    c = math.cos(a)

    _x = x * c + z * -s
    _z = x * s + z * c

    return (_x, y, _z)


def rotateZ(x, y, z, a):
    a = a * (pi / 180)  # convert to radians
    s = math.sin(a)
    c = math.cos(a)

    _x = x * c + y * s
    _y = x * -s + y * c

    return (_x, _y, z)


def rotateD(x, y, z, a, u=None):
    a = a * (pi / 180)  # convert to radians
    s = math.sin(a)
    c = math.cos(a)
    m = 1 - c

    if not u:
        u = [math.sqrt(3) / 3, math.sqrt(3) / 3, math.sqrt(3) / 3]

    _x = x * (c + u[0] * u[0] * m) + y * (u[0] * u[1] * m +
                                          u[2] * s) + z * (u[0] * u[2] * m - u[1] * s)
    _y = x * (u[0] * u[1] * m - u[2] * s) + y * \
        (c + u[1] * u[1] * m) + z * (u[1] * u[2] * m + u[0] * s)
    _z = x * (u[0] * u[2] * m + u[1] * s) + y * \
        (u[1] * u[2] * m - u[0] * s) + z * (c + u[2] * u[2] * m)

    return (_x, _y, _z)


def plotCube(a):
    C = 2
    s = 40
    for u in range(-s // 2, s // 2, 1):
        u = u / C
        for v in range(-s // 2, s // 2, 1):
            v = v / C
            w = s / (2 * C)

            # front
            (x, y, z) = rotateD(u, v, w, a)
            plot(x, y, z, '-')
            # right
            (x, y, z) = rotateD(w, u, v, a)
            plot(x, y, z, '~')
            # bottom
            (x, y, z) = rotateD(u, w, v, a)
            plot(x, y, z, "*")

            # back
            (x, y, z) = rotateD(u, v, -w, a)
            plot(x, y, z, ';')
            # left
            (x, y, z) = rotateD(-w, u, v, a)
            plot(x, y, z, '=')
            # top
            (x, y, z) = rotateD(u, -w, v, a)
            plot(x, y, z, '!')


def plotHCube(a):
    C = 2
    s = 40
    for u in range(-s // 2, s // 2, 1):
        u = u / C
        w = s / (2 * C)

        (x, y, z) = rotateD(u, w, w, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(u, -w, w, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(u, w, -w, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(u, -w, -w, a)
        plot(x, y, z, '#')

        (x, y, z) = rotateD(w, u, w, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(-w, u, w, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(w, u, -w, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(-w, u, -w, a)
        plot(x, y, z, '#')

        (x, y, z) = rotateD(w, w, u, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(-w, w, u, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(w, -w, u, a)
        plot(x, y, z, '#')
        (x, y, z) = rotateD(-w, -w, u, a)
        plot(x, y, z, '#')


for a in range(0, 2*360 + 1, 1):  # for every angle [0, 360]
    out = [[' ' for i in range(WIDTH)] for j in range(HEIGHT)]
    zBuffer = [[-1111 for i in range(WIDTH)] for j in range(HEIGHT)]

    plotCube(a)
    # time.sleep(0.08)
    draw()
