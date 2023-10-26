import math
import os
import time

(WIDTH, HEIGHT) = os.get_terminal_size()
pi = math.pi

out = [[' ' for i in range(WIDTH)] for j in range(HEIGHT)]

print(WIDTH, HEIGHT)

r = 5

t = 0
while t < 1:
    p = 2 * math.pi * t
    x = math.cos(p)
    y = math.sin(p)

    col = WIDTH / 2 + (x * r * 2.3 - 1)
    row = HEIGHT / 2 + (y * r - 1)

    out[round(row)][round(col)] = '#'
    t += 0.01


def draw():
    for row in range(HEIGHT):
        for col in range(WIDTH):
            print(out[row][col], end='')
        print()


draw()
