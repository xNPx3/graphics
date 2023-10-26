import numpy as np

# Rotate around X-axis
def X(a=0):
    return np.mat([
        [1, 0, 0],
        [0, np.cos(a), -np.sin(a)],
        [0, np.sin(a), np.cos(a)]
    ])

# Rotate around Y-axis
def Y(a=0):
    return np.mat([
        [np.cos(a), 0, np.sin(a)],
        [0, 1, 0],
        [-np.sin(a), 0, np.cos(a)]
    ])

# Rotate around Z-axis
def Z(a=0):
    return np.mat([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a), np.cos(a), 0],
        [0, 0, 1]
    ])

# Rotate around an arbitrary axis
def Axis(a, unit):
    (x, y, z) = unit.T
    sin = np.sin(a)
    cos = np.cos(a)
    mc = (1 - cos)
    return np.mat([
        [cos + x * x * mc,      x * y * mc - z * sin,   x * z * mc + y * sin],
        [x * y * mc + z * sin,  cos + y * y * mc,       y * z * mc - x * sin],
        [x * z * mc - y * sin,  y * z * mc + x * sin,   cos + z * z * mc]
    ])
