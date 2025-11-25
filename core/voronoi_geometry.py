from .geometry_utils import GeometryUtils
from .shapely_helper import ShapelyHelper

class VoronoiGeometry:
    def __init__(self, shapely_helper: ShapelyHelper):
        self.sh = shapely_helper

    def perpendicular_bisector(self, a, b, length=1000):
        a = GeometryUtils.to_np(a, self.sh.Point)
        b = GeometryUtils.to_np(b, self.sh.Point)

        m = GeometryUtils.midpoint(a, b)
        v = GeometryUtils.vec(a, b)
        p = GeometryUtils.perpendicular(v)
        p = GeometryUtils.normalize(p)

        p1 = m + length * GeometryUtils.np.array(p)
        p2 = m - length * GeometryUtils.np.array(p)

        return self.sh.LineString([tuple(p1), tuple(p2)])

    def half_plane_polygon(self, line, space, point):
        parts = self.sh.split(space, line)
        for poly in parts.geoms:
            if poly.contains(point):
                return poly
        raise ValueError("Reference point not inside split result")

    def signed_distance_to_line(self, point, line):
        a, b, c = line
        x, y = GeometryUtils.to_np(point)
        return a*x + b*y + c

    def intersect_segment_line(self, p1, p2, line):
        a, b, c = line
        p1 = GeometryUtils.to_np(p1)
        p2 = GeometryUtils.to_np(p2)

        d = p2 - p1
        denom = a*d[0] + b*d[1]
        if abs(denom) < 1e-12:
            return None

        t = -(a*p1[0] + b*p1[1] + c) / denom
        if not (0 <= t <= 1):
            return None

        ip = p1 + t * d
        return tuple(ip)

    def clip_polygon_by_halfplane(self, polygon, line, keep_positive=True):
        a, b, c = line

        if self.sh.Point and hasattr(polygon, "exterior"):
            coords = list(polygon.exterior.coords)[:-1]
            is_shapely = True
        else:
            coords = polygon
            is_shapely = False

        def inside(v):
            return (v >= 0) if keep_positive else (v <= 0)

        output = []
        n = len(coords)

        for i in range(n):
            curr = coords[i]
            prev = coords[i-1]

            curr_val = self.signed_distance_to_line(curr, line)
            prev_val = self.signed_distance_to_line(prev, line)

            curr_in = inside(curr_val)
            prev_in = inside(prev_val)

            if curr_in:
                if prev_in:
                    output.append(curr)
                else:
                    ip = self.intersect_segment_line(prev, curr, line)
                    if ip: output.append(ip)
                    output.append(curr)
            else:
                if prev_in:
                    ip = self.intersect_segment_line(prev, curr, line)
                    if ip: output.append(ip)

        if is_shapely:
            return self.sh.Polygon(output) if len(output) >= 3 else self.sh.Polygon()

        return output
