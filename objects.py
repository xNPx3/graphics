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

    return (obj, obj.copy())


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

    return (obj, obj.copy())


def circle(r, a=100):
    from rotations import X
    obj = np.array([[r, 0, -1]])

    for t in range(a+1):
        t = t / a
        p = np.pi * t
        x = np.cos(p) * r
        y = np.sin(p) * r

        obj = np.concatenate((obj, np.array([
            [x, y, 0],
            [-x, -y, 0],
        ])))

    return (obj, obj.copy())


def ball(r, a=100):
    from rotations import X, Y, Z
    obj = np.array([[r, 0, 0]])

    for t in range(a+1):
        t = t / a
        p = np.pi * t
        x = np.cos(p) * r
        y = np.sin(p) * r

        obj = np.concatenate((obj, np.array([
            [x, y, 0],
            [-x, -y, 0],

            [0, x, y],
            [0, -x, -y],
        ])))

    obj = np.concatenate((obj, np.dot(obj, Y(np.radians(90 / 2)))))

    return (obj, obj.copy())


class Object():
    pos = points = points_local = np.array([0, 0, 0])

    def __init__(self, func, *args):
        (p, pl) = func(*args)
        self.points = p
        self.points_local = pl

    def translate(self, delta: np.array):
        def _translate(p, d: np.array):
            return np.sum([p, np.array(d)], axis=0)
        self.points = np.apply_along_axis(_translate, 1, self.points, delta)
        self.pos = self.pos + delta

    def rotate(self, *rot):
        self.points_local = np.linalg.multi_dot([self.points_local, *rot])
        self.points = self.points_local
        self.translate(self.pos)
        

    def rotate_around(self, *rot):
        self.points = np.linalg.multi_dot([self.points, *rot])
        self.pos = np.linalg.multi_dot([self.pos, *rot])
