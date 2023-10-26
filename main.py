import math
import os
import time
import numpy as np

from numpy.linalg import multi_dot

from rotations import *
from objects import *


(WIDTH, HEIGHT) = os.get_terminal_size()
SHADE = "░▒▓█"
LIGHT_INTENSITY = 1
#SHADE = ''.join(_ * LIGHT_INTENSITY for _ in SHADE)

FRAME_BUFFER = np.full((HEIGHT, WIDTH), ' ')
Z_BUFFER = np.zeros((HEIGHT, WIDTH))
CURRENT_FRAME = 0
FRAMETIME = 0

SCALING = [1, 0.5]
CAMERA_POS = [0, 0, 0]
PLANE_POS = [0, 0, 1]
LIGHT_POS = [0, 0, 0]  # not implemented

# np.seterr(divide='ignore', invalid='ignore')


def rad(a):  # degrees to radians
    return a * (np.pi / 180)


def clearBuffers():  # clear frame buffers
    global FRAME_BUFFER, Z_BUFFER

    # FRAME_BUFFER = np.where(FRAME_BUFFER != ' ', ' ', ' ')

    FRAME_BUFFER = np.full((HEIGHT, WIDTH), ' ')
    Z_BUFFER = np.zeros((HEIGHT, WIDTH))


def draw():  # draw frame buffer to terminal
    global CURRENT_FRAME, FRAMETIME

    # dont print last row to prevent jittering
    for row in range(HEIGHT - 1):
        for col in range(WIDTH):
            print(FRAME_BUFFER[row][col], end='')
        print()

    clearBuffers()

    t = time.time()
    FPS = round(1 / (t - FRAMETIME))
    CURRENT_FRAME += 1
    FRAMETIME = t

    # bottom row for debugging
    print(f'{SHADE} | F:{CURRENT_FRAME} | FPS:{FPS} | {WIDTH}x{HEIGHT} | debug', end=' ')

    # cursor to home position (top left)
    print(f'\033[H', end='')


def draw_optimized():  # draw frame buffer to terminal (optimized)
    global CURRENT_FRAME, FRAMETIME

    # dont print last row to prevent jittering
    p = np.ravel(FRAME_BUFFER[:-1])
    print(''.join(p), end='')

    clearBuffers()

    t = time.time()
    FPS = round(1 / (t - FRAMETIME))
    CURRENT_FRAME += 1
    FRAMETIME = t

    # bottom row for debugging
    print(f'{SHADE} | F:{CURRENT_FRAME} | FPS:{FPS} | {WIDTH}x{HEIGHT} | debug', end=' ')

    # cursor to home position (top left)
    print(f'\033[H', end='')


def plot(points):
    def _plot(p, zmin, zmax, shading):
        col = row = -1

        (x, y, z) = p.T

        # center of screen, offset by scaled pos and camera pos
        col = int(WIDTH / 2 + x * SCALING[0] - CAMERA_POS[0] - 1)
        row = int(HEIGHT / 2 - y * SCALING[1] + CAMERA_POS[1] - 1)

        if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
            z_norm = ((z - zmin) / (zmax - zmin))
            if z_norm >= Z_BUFFER[row][col]:
                # TODO: light source position
                i = round(z_norm * shading)

                FRAME_BUFFER[row][col] = SHADE[i]
                Z_BUFFER[row][col] = z_norm

    zvalues = points[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)
    s = (len(SHADE) - 1)

    # apply function for every point
    np.apply_along_axis(_plot, 1, points, zmin, zmax, s)


def plotXYAxis():  # Draw the X and Y axises
    for row in range(HEIGHT):
        FRAME_BUFFER[row][WIDTH // 2] = '│'

    for col in range(WIDTH):
        FRAME_BUFFER[HEIGHT // 2][col] = '─'

    FRAME_BUFFER[HEIGHT // 2][col] = 'X'
    FRAME_BUFFER[0][WIDTH // 2] = 'Y'

    FRAME_BUFFER[HEIGHT // 2][WIDTH // 2] = '┼'


def translate(data, delta):  # cheap point translation function
    def _translate(p, d: np.array):
        return np.sum([p, np.array(d)], axis=0)
    return np.apply_along_axis(_translate, 1, data, delta)


def main():
    c1 = cube(20)
    c1 = translate(c1, [30, 0, 0])
    while CURRENT_FRAME < 100:
        c1 = multi_dot([c1, Y(rad(1))])
        plotXYAxis()
        plot(c1)
        draw_optimized()


if __name__ == "__main__":
    os.system('cls')
    print('\033[?25l', end='')

    main()

    print('\033[2J', end='\033[?25h')
