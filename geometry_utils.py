class GeometryUtils:
    import numpy as np

    @staticmethod
    def to_np(p, Point=None):
        if Point is not None and isinstance(p, Point):
            return GeometryUtils.np.array([p.x, p.y], dtype=float)

        a = GeometryUtils.np.array(p, dtype=float)
        if a.size != 2:
            raise ValueError("to_np expects a 2D point")
        return a.reshape(2,)

    @staticmethod
    def dist(a, b):
        a = GeometryUtils.to_np(a)
        b = GeometryUtils.to_np(b)
        return ((b - a) ** 2).sum() ** 0.5

    @staticmethod
    def midpoint(a, b):
        return (GeometryUtils.to_np(a) + GeometryUtils.to_np(b)) / 2.0

    @staticmethod
    def vec(a, b):
        a = GeometryUtils.to_np(a)
        b = GeometryUtils.to_np(b)
        return (b - a)

    @staticmethod
    def dot(u, v):
        return u[0]*v[0] + u[1]*v[1]

    @staticmethod
    def cross(u, v):
        return u[0]*v[1] - u[1]*v[0]

    @staticmethod
    def normalize(u):
        length = (u[0]**2 + u[1]**2)**0.5
        if length == 0:
            raise ValueError("zero-length vector")
        return (u[0]/length, u[1]/length)

    @staticmethod
    def perpendicular(u):
        return (-u[1], u[0])
