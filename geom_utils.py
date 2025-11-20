import numpy as np
try:
    from shapely.geometry import Point, LineString, Polygon
    from shapely.ops import split
    HAS_SHAPELY = True
except Exception:
    Point = None
    LineString = None
    Polygon = None
    def split(space, line):
        raise ImportError("shapely is required for geometric splitting")
    HAS_SHAPELY = False

def to_np(p):
    # Accept shapely Point when available, otherwise accept sequences/arrays
    if Point is not None and isinstance(p, Point):
        return np.array([p.x, p.y], dtype=float)
    # Allow numpy arrays, tuples or lists
    a = np.array(p, dtype=float)
    if a.size != 2:
        raise ValueError("to_np expects a 2D point-like input")
    return a.reshape(2,)

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


def signed_distance_to_line(point, line: tuple) -> float:
    """Return signed value a*x + b*y + c for line (a,b,c) and point.

    The sign indicates the side of the line; magnitude is proportional to distance.
    """
    a, b, c = line
    p = to_np(point)
    x, y = float(p[0]), float(p[1])
    return a * x + b * y + c


def intersect_segment_line(p1, p2, line: tuple):
    """Intersect segment p1->p2 with infinite line (a,b,c).

    Returns intersection point as (x, y) if it lies within the segment, otherwise None.
    """
    a, b, c = line
    p1 = to_np(p1)
    p2 = to_np(p2)
    dx, dy = p2 - p1
    denom = a * dx + b * dy
    if abs(denom) < 1e-12:
        return None
    t = -(a * p1[0] + b * p1[1] + c) / denom
    if t < -1e-12 or t > 1 + 1e-12:
        return None
    t = max(0.0, min(1.0, t))
    ip = p1 + t * (p2 - p1)
    return (float(ip[0]), float(ip[1]))


def clip_polygon_by_halfplane(polygon, line: tuple, keep_positive: bool = True):
    """Clip a polygon by a half-plane defined by line (a,b,c).

    polygon may be a sequence of (x,y) vertices (list/tuple) or a shapely `Polygon`.
    The `line` is a tuple (a, b, c) representing ax + by + c = 0. If `keep_positive`
    is True the side where ax+by+c >= 0 is kept, otherwise the <= 0 side is kept.

    Returns the clipped polygon in the same type as the input (list of points or
    shapely Polygon). If nothing remains, returns an empty list or an empty
    shapely `Polygon` respectively.
    """
    # Normalize input to a list of 2-tuples
    input_was_shapely = False
    if polygon is None:
        return Polygon() if HAS_SHAPELY else []
    # Detect shapely polygon by presence of exterior.coords (avoids dependency at import)
    if hasattr(polygon, 'exterior') and hasattr(getattr(polygon, 'exterior'), 'coords'):
        input_was_shapely = True
        poly_coords = list(polygon.exterior.coords)[:-1]
    else:
        poly_coords = [tuple(map(float, p)) for p in polygon]

    if not poly_coords:
        return Polygon() if input_was_shapely else []

    inside = (lambda v: v >= -1e-12) if keep_positive else (lambda v: v <= 1e-12)
    output = []
    n = len(poly_coords)
    for i in range(n):
        curr = poly_coords[i]
        prev = poly_coords[i - 1]
        curr_val = signed_distance_to_line(curr, line)
        prev_val = signed_distance_to_line(prev, line)
        curr_inside = inside(curr_val)
        prev_inside = inside(prev_val)
        if curr_inside:
            if prev_inside:
                output.append(curr)
            else:
                ip = intersect_segment_line(prev, curr, line)
                if ip is not None:
                    output.append(ip)
                output.append(curr)
        else:
            if prev_inside:
                ip = intersect_segment_line(prev, curr, line)
                if ip is not None:
                    output.append(ip)

    if input_was_shapely:
        if len(output) < 3:
            return Polygon()
        return Polygon(output)
    return output
