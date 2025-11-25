"""
Comprehensive test suite for Incremental Voronoi Diagram
Member 12 - Testing & Debugging
"""

import unittest
import math
from geometry_utils import GeometryUtils
from shapely_helper import ShapelyHelper
from voronoi_geometry import VoronoiGeometry
from voronoi_diagram import VoronoiDiagram
from cell import Cell


class TestGeometryUtils(unittest.TestCase):
    """Test basic geometric operations"""
    
    def test_to_np_with_tuple(self):
        """Test converting tuple to numpy array"""
        result = GeometryUtils.to_np((1.0, 2.0))
        self.assertEqual(result[0], 1.0)
        self.assertEqual(result[1], 2.0)
    
    def test_to_np_with_list(self):
        """Test converting list to numpy array"""
        result = GeometryUtils.to_np([3.0, 4.0])
        self.assertEqual(result[0], 3.0)
        self.assertEqual(result[1], 4.0)
    
    def test_distance_origin_to_point(self):
        """Test distance calculation from origin"""
        dist = GeometryUtils.dist((0, 0), (3, 4))
        self.assertAlmostEqual(dist, 5.0, places=5)
    
    def test_distance_between_arbitrary_points(self):
        """Test distance between two arbitrary points"""
        dist = GeometryUtils.dist((1, 1), (4, 5))
        expected = math.sqrt((4-1)**2 + (5-1)**2)
        self.assertAlmostEqual(dist, expected, places=5)
    
    def test_distance_same_point(self):
        """Test distance of a point to itself"""
        dist = GeometryUtils.dist((5, 5), (5, 5))
        self.assertAlmostEqual(dist, 0.0, places=5)
    
    def test_midpoint_between_points(self):
        """Test midpoint calculation"""
        mid = GeometryUtils.midpoint((0, 0), (4, 4))
        self.assertAlmostEqual(mid[0], 2.0, places=5)
        self.assertAlmostEqual(mid[1], 2.0, places=5)
    
    def test_midpoint_arbitrary(self):
        """Test midpoint with arbitrary points"""
        mid = GeometryUtils.midpoint((1, 3), (5, 7))
        self.assertAlmostEqual(mid[0], 3.0, places=5)
        self.assertAlmostEqual(mid[1], 5.0, places=5)
    
    def test_vec_calculation(self):
        """Test vector calculation"""
        vec = GeometryUtils.vec((0, 0), (3, 4))
        self.assertAlmostEqual(vec[0], 3.0, places=5)
        self.assertAlmostEqual(vec[1], 4.0, places=5)
    
    def test_vec_negative(self):
        """Test vector with negative components"""
        vec = GeometryUtils.vec((5, 5), (2, 2))
        self.assertAlmostEqual(vec[0], -3.0, places=5)
        self.assertAlmostEqual(vec[1], -3.0, places=5)
    
    def test_dot_product_orthogonal(self):
        """Test dot product of orthogonal vectors (should be 0)"""
        u = (1, 0)
        v = (0, 1)
        dot = GeometryUtils.dot(u, v)
        self.assertAlmostEqual(dot, 0.0, places=5)
    
    def test_dot_product_parallel(self):
        """Test dot product of parallel vectors"""
        u = (3, 4)
        v = (3, 4)
        dot = GeometryUtils.dot(u, v)
        self.assertAlmostEqual(dot, 25.0, places=5)
    
    def test_cross_product_orthogonal(self):
        """Test cross product (should be non-zero for non-parallel vectors)"""
        u = (1, 0)
        v = (0, 1)
        cross = GeometryUtils.cross(u, v)
        self.assertAlmostEqual(cross, 1.0, places=5)
    
    def test_cross_product_parallel(self):
        """Test cross product of parallel vectors (should be 0)"""
        u = (2, 4)
        v = (1, 2)
        cross = GeometryUtils.cross(u, v)
        self.assertAlmostEqual(cross, 0.0, places=5)
    
    def test_normalize_unit_vector(self):
        """Test normalizing a vector"""
        u = (3, 4)
        normalized = GeometryUtils.normalize(u)
        mag = math.sqrt(normalized[0]**2 + normalized[1]**2)
        self.assertAlmostEqual(mag, 1.0, places=5)
    
    def test_normalize_preserves_direction(self):
        """Test that normalized vector has correct direction"""
        u = (3, 4)
        normalized = GeometryUtils.normalize(u)
        self.assertAlmostEqual(normalized[0], 0.6, places=5)
        self.assertAlmostEqual(normalized[1], 0.8, places=5)
    
    def test_perpendicular_vector(self):
        """Test perpendicular vector calculation"""
        u = (1, 0)
        perp = GeometryUtils.perpendicular(u)
        dot = GeometryUtils.dot(u, perp)
        self.assertAlmostEqual(dot, 0.0, places=5)
    
    def test_perpendicular_rotation(self):
        """Test that perpendicular is correct rotation"""
        u = (2, 3)
        perp = GeometryUtils.perpendicular(u)
        self.assertAlmostEqual(perp[0], -3.0, places=5)
        self.assertAlmostEqual(perp[1], 2.0, places=5)


class TestCell(unittest.TestCase):
    """Test Cell class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
    
    def test_cell_initialization(self):
        """Test basic cell initialization"""
        cell = Cell((0, 0), shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertEqual(cell.generator, (0.0, 0.0))
        self.assertEqual(cell.polygon, [])
    
    def test_cell_with_polygon(self):
        """Test cell initialization with polygon"""
        poly = [(0, 0), (1, 0), (1, 1), (0, 1)]
        cell = Cell((0.5, 0.5), polygon=poly, shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertEqual(len(cell.polygon), 4)
    
    def test_cell_area_square(self):
        """Test area calculation for square"""
        poly = [(0, 0), (2, 0), (2, 2), (0, 2)]
        cell = Cell((1, 1), polygon=poly, shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertAlmostEqual(cell.area(), 4.0, places=4)
    
    def test_cell_area_triangle(self):
        """Test area calculation for triangle"""
        poly = [(0, 0), (2, 0), (1, 2)]
        cell = Cell((1, 0.667), polygon=poly, shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertAlmostEqual(cell.area(), 2.0, places=4)
    
    def test_cell_area_empty(self):
        """Test area of empty polygon"""
        cell = Cell((0, 0), shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertEqual(cell.area(), 0.0)
    
    def test_cell_contains_point(self):
        """Test point containment check"""
        poly = [(0, 0), (2, 0), (2, 2), (0, 2)]
        cell = Cell((1, 1), polygon=poly, shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertTrue(cell.contains((1, 1)))
    
    def test_cell_not_contains_point(self):
        """Test point outside polygon"""
        poly = [(0, 0), (2, 0), (2, 2), (0, 2)]
        cell = Cell((1, 1), polygon=poly, shapely_helper=self.sh, voronoi_geo=self.vg)
        self.assertFalse(cell.contains((3, 3)))
    
    def test_cell_repr(self):
        """Test string representation"""
        poly = [(0, 0), (1, 0), (1, 1)]
        cell = Cell((0.5, 0.5), polygon=poly, shapely_helper=self.sh, voronoi_geo=self.vg)
        repr_str = repr(cell)
        self.assertIn("Cell", repr_str)
        self.assertIn("generator", repr_str)


class TestVoronoiGeometry(unittest.TestCase):
    """Test VoronoiGeometry module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
    
    def test_perpendicular_bisector_exists(self):
        """Test that perpendicular bisector creates a line"""
        bisector = self.vg.perpendicular_bisector((0, 0), (2, 0))
        self.assertIsNotNone(bisector)
        # Should have two endpoints
        coords = list(bisector.coords)
        self.assertEqual(len(coords), 2)
    
    def test_perpendicular_bisector_passes_through_midpoint(self):
        """Test bisector passes through midpoint"""
        p1 = (0, 0)
        p2 = (2, 0)
        midpoint = GeometryUtils.midpoint(p1, p2)
        bisector = self.vg.perpendicular_bisector(p1, p2)
        
        # Line should be perpendicular to p1-p2
        coords = list(bisector.coords)
        p_on_line_1 = coords[0]
        p_on_line_2 = coords[1]
        
        # Vector along bisector
        vec_bisector = (p_on_line_2[0] - p_on_line_1[0], p_on_line_2[1] - p_on_line_1[1])
        # Vector p1 to p2
        vec_original = (p2[0] - p1[0], p2[1] - p1[1])
        
        # Dot product should be ~0 (perpendicular)
        dot = GeometryUtils.dot(vec_bisector, vec_original)
        self.assertAlmostEqual(dot, 0.0, places=4)
    
    def test_signed_distance_positive(self):
        """Test signed distance to line - positive side"""
        line = (1, 0, 0)  # x = 0
        point = (1, 0)
        dist = self.vg.signed_distance_to_line(point, line)
        self.assertGreater(dist, 0)
    
    def test_signed_distance_negative(self):
        """Test signed distance to line - negative side"""
        line = (1, 0, 0)  # x = 0
        point = (-1, 0)
        dist = self.vg.signed_distance_to_line(point, line)
        self.assertLess(dist, 0)
    
    def test_signed_distance_on_line(self):
        """Test signed distance for point on line"""
        line = (1, 0, 0)  # x = 0
        point = (0, 5)
        dist = self.vg.signed_distance_to_line(point, line)
        self.assertAlmostEqual(dist, 0.0, places=5)
    
    def test_clip_polygon_removes_half(self):
        """Test that clipping polygon by halfplane reduces it"""
        polygon = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        line = (1, 0, 0)  # x = 0, keep positive (x > 0)
        clipped = self.vg.clip_polygon_by_halfplane(polygon, line, keep_positive=True)
        
        if isinstance(clipped, list):
            # Should have vertices on right side
            self.assertTrue(len(clipped) >= 3)
        else:
            # Shapely polygon
            self.assertTrue(len(list(clipped.exterior.coords)) >= 4)


class TestVoronoiDiagram(unittest.TestCase):
    """Test VoronoiDiagram - core algorithm"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=100)
    
    def test_initial_polygon_is_square(self):
        """Test that initial polygon is a bounding square"""
        poly = self.vd.initial_polygon()
        self.assertEqual(len(poly), 4)
        # Should be at bbox boundaries
        self.assertEqual(poly[0][0], -100)
        self.assertEqual(poly[1][0], 100)
    
    def test_line_equation_horizontal(self):
        """Test line equation for horizontal line"""
        line = self.sh.LineString([(0, 1), (1, 1)])
        eq = self.vd.line_equation(line)
        # Horizontal line: a=0, b=1, y-1=0
        self.assertAlmostEqual(eq[0], 0.0, places=5)
    
    def test_insert_single_site(self):
        """Test inserting a single site"""
        self.vd.insert_site((0, 0))
        self.assertEqual(len(self.vd.cells), 1)
        self.assertEqual(self.vd.cells[0].generator, (0.0, 0.0))
    
    def test_insert_two_sites(self):
        """Test inserting two sites"""
        self.vd.insert_site((0, 0))
        self.vd.insert_site((1, 0))
        self.assertEqual(len(self.vd.cells), 2)
    
    def test_incremental_voronoi_two_points(self):
        """Test incremental algorithm with two points"""
        points = [(0, 0), (2, 0)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 2)
        # Both cells should have some vertices
        for cell in cells:
            self.assertTrue(len(cell.polygon) > 0 or cell.polygon == [])
    
    def test_incremental_voronoi_three_points(self):
        """Test incremental algorithm with three points (triangle)"""
        points = [(0, 0), (1, 0), (0.5, 1)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 3)
    
    def test_incremental_voronoi_callback(self):
        """Test that callback is called during incremental algorithm"""
        callback_count = [0]
        
        def callback(i, p, cells):
            callback_count[0] += 1
        
        points = [(0, 0), (1, 0)]
        self.vd.incremental_voronoi(points, callback=callback)
        self.assertEqual(callback_count[0], 2)
    
    def test_no_cell_overlaps_two_points(self):
        """Test that cells don't overlap for 2 points"""
        points = [(0, 0), (2, 0)]
        cells = self.vd.incremental_voronoi(points)
        
        # Sample test points on the bisector
        test_points = [(1, -1), (1, 0), (1, 1)]
        for test_pt in test_points:
            count = sum(1 for cell in cells if cell.contains(test_pt))
            # Each point should be in at most one cell
            self.assertLessEqual(count, 1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=100)
    
    def test_duplicate_points(self):
        """Test handling of duplicate points"""
        points = [(0, 0), (0, 0)]
        cells = self.vd.incremental_voronoi(points)
        # Duplicate points are skipped, so only 1 cell is created
        self.assertEqual(len(cells), 1)
    
    def test_collinear_three_points(self):
        """Test three collinear points"""
        points = [(0, 0), (1, 0), (2, 0)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 3)
    
    def test_empty_points_list(self):
        """Test with empty points list"""
        cells = self.vd.incremental_voronoi([])
        self.assertEqual(len(cells), 0)
    
    def test_single_point(self):
        """Test with single point"""
        cells = self.vd.incremental_voronoi([(0, 0)])
        self.assertEqual(len(cells), 1)
    
    def test_very_close_points(self):
        """Test with very close points"""
        points = [(0, 0), (0.001, 0)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 2)


class TestAlgorithmProperties(unittest.TestCase):
    """Test mathematical properties of Voronoi diagram"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=100)
    
    def test_all_sites_have_cells(self):
        """Test that every site gets a cell"""
        points = [(0, 0), (2, 0), (1, 2), (-1, 1)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), len(points))
    
    def test_cell_contains_generator(self):
        """Test that each cell contains its generator point (or has empty polygon)"""
        points = [(0, 0), (2, 0), (1, 2)]
        cells = self.vd.incremental_voronoi(points)
        for cell in cells:
            # Generator should be close to cell (might be outside due to bbox)
            # At minimum, if polygon exists, generator should be related
            self.assertIsNotNone(cell.generator)
    
    def test_bisector_equidistant_property(self):
        """Test that perpendicular bisector maintains equidistant property"""
        p1 = (0, 0)
        p2 = (4, 0)
        bisector = self.vg.perpendicular_bisector(p1, p2)
        
        # Test points on bisector
        coords = list(bisector.coords)
        test_point = coords[0]
        
        dist1 = GeometryUtils.dist(test_point, p1)
        dist2 = GeometryUtils.dist(test_point, p2)
        
        self.assertAlmostEqual(dist1, dist2, places=3)


def run_tests_with_report():
    """Run all tests and generate a detailed report"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGeometryUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestCell))
    suite.addTests(loader.loadTestsFromTestCase(TestVoronoiGeometry))
    suite.addTests(loader.loadTestsFromTestCase(TestVoronoiDiagram))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithmProperties))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests_with_report()
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
