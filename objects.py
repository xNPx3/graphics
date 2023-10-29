import numpy as np


def cubeV(s): 
    """
        Cube edges
    """
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


def cube(s):
    """
        Cube with filled faces
    """
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
    """
        2D circle
    """

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


def sphere(r, a=100):
    """
        3D Sphere (not filled)
    """
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


def tetrahedron(s):
    """
        3D tetrahedron
    """
    from rotations import X
    oos = 1 / np.sqrt(2)
    obj = np.array([[0, 0, oos * s]])
    for t in range(-s, s, 1):
        u = t / 2 + s / 2
        v = t / 2 - s / 2
        obj = np.concatenate((obj, np.array([
            [0, t, oos * s],
            [t, 0, -oos * s],

            [v, u, t * oos],
            [-v, u, t * oos],
            [v, -u, t * oos],
            [-v, -u, t * oos],
        ])))

    obj = np.dot(obj, X(np.radians(35)))

    return (obj, obj.copy())


def tetrahedron2(s):
    h = s ** 2
    obj = np.array([
        [0, 0, 0],
        [s, 0, 0],
        [s / 2, np.sqrt(h + h/4), 0],
        [s / 2, 0, np.sqrt(h + h/4)]
    ])


class Object():
    """
        Initializes an object from a points function
    """
    pos = points = points_local = np.array([0, 0, 0])

    def __init__(self, func, *args):
        (p, pl) = func(*args)
        self.points = p
        self.points_local = pl

    def translate(self, delta: np.array):
        """
            Translates the object by a vector
        """
        def _translate(p, d: np.array):
            return np.sum([p, np.array(d)], axis=0)
        self.points = np.apply_along_axis(_translate, 1, self.points, delta)
        self.pos = self.pos + delta

    def rotate(self, *rot):  # translate - rotate - translate
        """
            Rotates the object in local space
        """
        self.points_local = np.linalg.multi_dot([self.points_local, *rot])
        self.points = self.points_local
        _pos = self.pos.copy()
        self.pos = np.array([0, 0, 0])
        self.translate(_pos)

    def rotate_world(self, *rot):
        """
            Rotates the object in world space
        """
        self.points = np.linalg.multi_dot([self.points, *rot])
        self.pos = np.linalg.multi_dot([self.pos, *rot])
