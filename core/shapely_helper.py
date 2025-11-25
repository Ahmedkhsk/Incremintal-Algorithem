class ShapelyHelper:
    def __init__(self):
        try:
            from shapely.geometry import Point, LineString, Polygon
            from shapely.ops import split
            self.Point = Point
            self.LineString = LineString
            self.Polygon = Polygon
            self.split = split
            self.has_shapely = True
        except:
            self.Point = None
            self.LineString = None
            self.Polygon = None
            self.split = None
            self.has_shapely = False
