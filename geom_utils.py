import numpy as np
from shapely.geometry import Point

def to_np(p):
    if isinstance(p, Point):
        return np.array([p.x, p.y], dtype=float)
    return np.array(p, dtype=float).reshape(2,)

def dist(a, b):
    a = to_np(a)
    b = to_np(b)
    x1, y1 = a
    x2, y2 = b
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def midpoint(a, b):
    a = to_np(a)
    b = to_np(b)
    return (a + b) / 2.0

def vec(a, b):
    a = to_np(a)
    b = to_np(b)
    x1, y1 = a
    x2, y2 = b
    return (x2 - x1, y2 - y1)

def dot(u, v):
    ux, uy = u
    vx, vy = v
    return ux*vx + uy*vy

def cross(u, v):
    ux, uy = u
    vx, vy = v
    return ux*vy - uy*vx

def normalize(u):
    ux, uy = u
    length = (ux**2 + uy**2)**0.5
    if length == 0:
        raise ValueError("zero-length vector")
    return (ux/length, uy/length)

def perpendicular(u):
    ux, uy = u
    return (-uy, ux)
