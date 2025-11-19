import numpy as np
from shapely.geometry import Point,LineString

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
""" Perpendicular Bisector Function """
def perpendicular_bisector(a, b, length=1000):
    a= to_np(a)
    b= to_np(b)
    m= midpoint(a,b)
    v= vec(a,b)
    p= perpendicular(v)
    p= normalize(p)
    p1= m+ length * np.array(p)
    p2= m - length * np.array(p)
    return LineString([tuple(np.round(p1, 3)), tuple(np.round(p2, 3))])

from shapely.ops import split
from shapely.geometry import Polygon, Point, LineString, GeometryCollection


def half_plane_polygon(line: LineString, space: Polygon, point: Point) -> Polygon:
    """
    Splits a polygon and returns the half containing the reference point.
    Args:
        line (LineString): The line used for splitting.
        space (Polygon): The polygon to be split.
        point (Point): The reference point used to select the correct half.

    Returns:
        Polygon: The resulting polygon that contains the reference point.
    """
    parts = split(space, line)

    if len(parts.geoms) == 1:
        if parts.geoms[0].contains(point):
            return parts.geoms[0]
        else:
            return space
        
    for poly in parts.geoms:
        if poly.intersects(point):
            return poly

    raise ValueError("The reference point does not fall inside any of the polygons after the split")
