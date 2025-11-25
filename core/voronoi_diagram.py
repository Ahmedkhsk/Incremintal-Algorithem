from core.cell import Cell
from core.geometry_utils import GeometryUtils

class VoronoiDiagram:
    def __init__(self, shapely_helper, voronoi_geo, bbox=10000):
        self.cells = []
        self.sh = shapely_helper
        self.vg = voronoi_geo
        self.bbox = bbox

    def initial_polygon(self):
        b = self.bbox
        return [
            (-b, -b),
            ( b, -b),
            ( b,  b),
            (-b,  b)
        ]

    def line_equation(self, line):
        (x1, y1), (x2, y2) = line.coords
        a = y1 - y2
        b = x2 - x1
        c = x1*y2 - x2*y1
        return (a, b, c)

    def choose_halfplane_side(self, new_point, old_point, bisector):
        new_p = GeometryUtils.to_np(new_point)
        line = self.line_equation(bisector)
        val = self.vg.signed_distance_to_line(new_p, line)
        return val >= 0

    def insert_site(self, point):
        # Check if this point is a duplicate of an existing site
        for existing_cell in self.cells:
            dist = GeometryUtils.dist(existing_cell.generator, point)
            if dist < 1e-10:
                # Skip duplicate points
                return existing_cell

        new_cell = Cell(
            point,
            polygon=self.initial_polygon(),
            shapely_helper=self.sh,
            voronoi_geo=self.vg
        )

        for cell in self.cells:
            if not cell.polygon:
                continue

            bisector = self.vg.perpendicular_bisector(cell.generator, point)
            line = self.line_equation(bisector)

            keep_positive_for_old = self.choose_halfplane_side(
                new_point=cell.generator,
                old_point=point,
                bisector=bisector
            )

            cell.clip_with_halfplane(line, keep_positive_for_old)
            new_cell.clip_with_halfplane(line, not keep_positive_for_old)

        self.cells.append(new_cell)
        return new_cell

    def incremental_voronoi(self, points, callback=None):
        pts = [tuple(map(float, p)) for p in points]
        self.cells = []

        for i, p in enumerate(pts):
            new_cell = self.insert_site(p)
            if callback:
                callback(i, p, self.cells)

        return self.cells
