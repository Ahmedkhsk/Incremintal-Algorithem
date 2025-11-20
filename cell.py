class Cell:
    def __init__(self, generator, polygon=None, shapely_helper=None, voronoi_geo=None):
        self.sh = shapely_helper
        self.vg = voronoi_geo
        self.generator = tuple(map(float, generator))

        if polygon is None:
            self.polygon = []
        else:
            self.update_polygon(polygon)

    def update_polygon(self, polygon):
        if polygon is None:
            self.polygon = []
            return

        if self.sh and hasattr(polygon, 'exterior'):
            self.polygon = list(polygon.exterior.coords)[:-1]
        else:
            self.polygon = [tuple(map(float, p)) for p in polygon]

    def area(self):
        if not self.polygon:
            return 0.0

        if self.sh and self.sh.has_shapely:
            return float(self.sh.Polygon(self.polygon).area)

        pts = self.polygon
        s = 0.0
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            s += x1*y2 - x2*y1
        return abs(s) * 0.5

    def contains(self, point):
        p = tuple(map(float, point))

        if not self.polygon:
            return False

        if self.sh and self.sh.has_shapely:
            return self.sh.Polygon(self.polygon).contains(self.sh.Point(p))

        x, y = p
        inside = False
        pts = self.polygon
        n = len(pts)
        for i in range(n):
            xi, yi = pts[i]
            xj, yj = pts[(i + 1) % n]
            intersect = ((yi > y) != (yj > y)) and \
                        (x < (xj - xi) * (y - yi) / (yj - yi + 1e-18) + xi)
            if intersect:
                inside = not inside

        return inside

    def clip_with_halfplane(self, line, keep_positive=True):
        if not self.vg:
            raise RuntimeError("VoronoiGeometry instance not attached to Cell")

        clipped = self.vg.clip_polygon_by_halfplane(self.polygon, line, keep_positive)
        self.update_polygon(clipped)
        return self.polygon

    def __repr__(self):
        return f"Cell(generator={self.generator}, vertices={len(self.polygon)})"
