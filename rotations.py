import numpy as np


def X(a=0):  # Rotate around X-axis
    return np.array([
        [1, 0, 0],
        [0, np.cos(a), -np.sin(a)],
        [0, np.sin(a), np.cos(a)]
    ])


def Y(a=0):  # Rotate around Y-axis
    return np.array([
        [np.cos(a), 0, np.sin(a)],
        [0, 1, 0],
        [-np.sin(a), 0, np.cos(a)]
    ])


def Z(a=0):  # Rotate around Z-axis
    return np.array([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a), np.cos(a), 0],
        [0, 0, 1]
    ])


def Axis(a, unit):  # Rotate around an arbitrary axis
    (x, y, z) = unit.T
    sin = np.sin(a)
    cos = np.cos(a)
    mc = (1 - cos)
    return np.array([
        [cos + x * x * mc,      x * y * mc - z * sin,   x * z * mc + y * sin],
        [x * y * mc + z * sin,  cos + y * y * mc,       y * z * mc - x * sin],
        [x * z * mc - y * sin,  y * z * mc + x * sin,   cos + z * z * mc]
    ])
