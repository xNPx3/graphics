import numpy as np


def cubeV(s):  # Cube with only the vertices
    # dividing by two so the points are put around (0, 0, 0)
    v = s // 2
    obj = np.array([[v, v, v]])

    for u in range(-v, v, 1):
        # all cube vertices
        obj = np.concatenate((obj, np.array([
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


def cube(s):  # Normal cube
    w = s // 2
    obj = np.array([[w, w, w]])

    for u in range(-w, w, 1):
        for v in range(-w, w, 1):
            # six faces
            obj = np.concatenate((obj, np.array([
                [u, v, w],
                [u, w, v],
                [w, u, v],

                [u, v, -w],
                [u, -w, v],
                [-w, u, v],
            ])))

    return obj
