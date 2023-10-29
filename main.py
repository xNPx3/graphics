import math
import os
import time
import numpy as np

from rotations import *
from objects import *


(WIDTH, HEIGHT) = os.get_terminal_size()
W2, H2 = WIDTH // 2, HEIGHT // 2
SHADE = ['░', '▒', '▓', '█']
SHADE_LEN = len(SHADE) - 1

FRAME_BUFFER = np.full((HEIGHT, WIDTH), ' ')
Z_BUFFER = np.zeros((HEIGHT, WIDTH))
CURRENT_FRAME = 0
FRAMETIME = 0

SCALING = [1, 0.5]
CAMERA_POS = [0, 0, 0]

FOV = 70
ASPECT_RATIO = WIDTH / HEIGHT

focal_length = 1 / np.tan(np.deg2rad(FOV / 2))

# np.seterr(divide='ignore', invalid='ignore')


def rad(a):
    """
        Alias for np.radians()
    """
    return np.radians(a)


def clearBuffers():
    """
        Clears the frame- and z-buffer
    """
    global FRAME_BUFFER, Z_BUFFER

    # FRAME_BUFFER = np.where(FRAME_BUFFER != ' ', ' ', ' ')

    FRAME_BUFFER = np.full((HEIGHT, WIDTH), ' ')
    Z_BUFFER = np.zeros((HEIGHT, WIDTH))


def draw():
    """
        Prints the current frame to the terminal
    """
    global CURRENT_FRAME, FRAMETIME

    # dont print last row to prevent jittering
    F = np.ravel(FRAME_BUFFER[:-1])
    p = ''.join(F)
    print(p, end='')

    clearBuffers()

    t = time.time()
    FPS = round(1 / (t - FRAMETIME))
    CURRENT_FRAME += 1
    FRAMETIME = t

    # bottom row for debugging
    print(f'{"".join(s for s in SHADE)} | F:{CURRENT_FRAME} | FPS:{FPS} | {WIDTH}x{HEIGHT}', end=' ')

    # cursor to home position (top left)
    print(f'\033[H', end='')


def plot(points):
    """
        Array of points in world space -> characters in the frame-buffer
    """
    def _plot(P, MIN, MAX):
        (x, y, z, *w) = P.T

        # center of screen, offset by scaled pos and camera pos
        col = int(W2 + x * SCALING[0] - CAMERA_POS[0] - 1)
        row = int(H2 - y * SCALING[1] + CAMERA_POS[1] - 1)

        if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
            NORM = ((z - MIN) / (MAX - MIN))
            if NORM >= Z_BUFFER[row][col]:
                #LIGHT_DIST = np.linalg.norm(LIGHT_POS-P)

                i = round(NORM * SHADE_LEN)

                FRAME_BUFFER[row][col] = SHADE[i]
                Z_BUFFER[row][col] = NORM

    zvalues = points[:, 2]
    zMin = np.min(zvalues)
    zMax = np.max(zvalues)

    # apply function for every point (slow)
    np.apply_along_axis(_plot, 1, points, zMin, zMax)


def plotp(points):
    """
    Array of points in world space -> characters in the frame-buffer with perspective projection
    """
    def _plot(P, MIN, MAX):
        (x, y, z, *w) = P.T

        # Apply perspective projection
        xp = (focal_length * x) / z * 20
        yp = (focal_length * y) / z * 20

        # Translate and scale the projected point
        col = int(W2 + xp * SCALING[0] - CAMERA_POS[0] - 1)
        row = int(H2 - yp * SCALING[1] + CAMERA_POS[1] - 1)

        if (0 <= col < WIDTH) and (0 <= row < HEIGHT):
            NORM = ((z - MAX) / (MIN - MAX))
            if NORM >= Z_BUFFER[row][col]:
                i = round(NORM * SHADE_LEN)
                FRAME_BUFFER[row][col] = SHADE[i]
                Z_BUFFER[row][col] = NORM

    zvalues = points[:, 2]
    zMin = np.min(zvalues)
    zMax = np.max(zvalues)

    # apply function for every point (slow)
    np.apply_along_axis(_plot, 1, points, zMin, zMax)


def plotXYAxis():
    """
        Draws the X and Y axis
    """
    for row in range(HEIGHT):
        FRAME_BUFFER[row][W2 - 1] = '│'

    for col in range(WIDTH):
        FRAME_BUFFER[H2 - 1][col] = '─'

    FRAME_BUFFER[H2 - 1][col] = 'X'
    FRAME_BUFFER[0][W2 - 1] = 'Y'

    FRAME_BUFFER[H2 - 1][W2 - 1] = '┼'


def plot_optimized(points):  # optimized by chatgpt
    zvalues = points[:, 2]
    zmin = np.min(zvalues)
    zmax = np.max(zvalues)

    # Precompute constants
    z_diff = zmax - zmin
    z_buffer = (points[:, 2] - zmin) / z_diff
    i_values = (z_buffer * (len(SHADE) - 1)).round().astype(int)

    # Calculate col and row indices
    x = points[:, 0]
    y = points[:, 1]
    col = ((x * SCALING[0] - CAMERA_POS[0] - 1) + W2).astype(int)
    row = (H2 - (y * SCALING[1] + CAMERA_POS[1] - 1)).astype(int)

    # Create masks for valid indices
    valid_col = (col >= 0) & (col < WIDTH)
    valid_row = (row >= 0) & (row < HEIGHT)
    valid_indices = valid_col & valid_row

    # Update frame and z buffers using boolean indexing
    frame_indices = valid_indices & (
        z_buffer >= Z_BUFFER[row[valid_indices], col[valid_indices]])
    Z_BUFFER[row[valid_indices][frame_indices], col[valid_indices]
             [frame_indices]] = z_buffer[frame_indices]

    # Use i_values as an index to print characters from SHADE
    FRAME_BUFFER[row[valid_indices][frame_indices], col[valid_indices]
                 [frame_indices]] = [SHADE[i] for i in i_values[frame_indices]]


def main():
    cube = Object(cubeV, 20)
    cube.translate([20, 5, 20])

    while CURRENT_FRAME < 100:
        cube.rotate(Y(rad(1)))
        plotXYAxis()
        plot(cube.points)
        draw()


if __name__ == "__main__":
    os.system('cls')
    print('\033[?25l', end='')

    main()

    print('\033[2J', end='\033[?25h')
