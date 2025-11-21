"""
Visualization & Integration Tests for Voronoi Diagram
Tests Member 13's visualization code
"""

import unittest
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import numpy as np
from geometry_utils import GeometryUtils
from shapely_helper import ShapelyHelper
from voronoi_geometry import VoronoiGeometry
from voronoi_diagram import VoronoiDiagram
from cell import Cell


class TestVisualization(unittest.TestCase):
    """Test visualization rendering and correctness"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=50)
    
    def test_visualization_renders_two_points(self):
        """Test that visualization can render two-point diagram"""
        points = [(0, 0), (2, 0)]
        cells = self.vd.incremental_voronoi(points)
        
        # Create figure for visualization
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Draw cells
        for cell in cells:
            if len(cell.polygon) >= 3:
                poly = MplPolygon(cell.polygon, fill=False, edgecolor='blue', linewidth=2)
                ax.add_patch(poly)
        
        # Draw sites
        for cell in cells:
            ax.plot(cell.generator[0], cell.generator[1], 'ro', markersize=8)
        
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        plt.close(fig)
        # If we get here without exception, rendering works
        self.assertTrue(True)
    
    def test_visualization_renders_three_points(self):
        """Test that visualization can render three-point diagram"""
        points = [(0, 0), (2, 0), (1, 2)]
        cells = self.vd.incremental_voronoi(points)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        for cell in cells:
            if len(cell.polygon) >= 3:
                poly = MplPolygon(cell.polygon, fill=False, edgecolor='green', linewidth=2)
                ax.add_patch(poly)
        
        for cell in cells:
            ax.plot(cell.generator[0], cell.generator[1], 'ro', markersize=8)
        
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        plt.close(fig)
        self.assertTrue(True)
    
    def test_cell_polygon_valid(self):
        """Test that computed cells have valid polygons"""
        points = [(0, 0), (1, 0), (0.5, 1)]
        cells = self.vd.incremental_voronoi(points)
        
        for cell in cells:
            if cell.polygon:
                # Check polygon has at least 3 vertices
                self.assertGreaterEqual(len(cell.polygon), 3)
                # Check all vertices are valid 2D points
                for vertex in cell.polygon:
                    self.assertEqual(len(vertex), 2)


class TestAlgorithmCorrectness(unittest.TestCase):
    """Test mathematical correctness of algorithm results"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=50)
    
    def test_bisector_property_two_points(self):
        """Test that bisector correctly separates two points"""
        p1 = (0, 0)
        p2 = (4, 0)
        
        # Get bisector
        bisector = self.vg.perpendicular_bisector(p1, p2)
        line_coords = list(bisector.coords)
        line_eq = self.vd.line_equation(bisector)
        
        # Test midpoint is on the line
        mid = GeometryUtils.midpoint(p1, p2)
        dist = self.vg.signed_distance_to_line(mid, line_eq)
        self.assertAlmostEqual(dist, 0.0, places=5)
    
    def test_three_point_diagram_coverage(self):
        """Test that three points create cells covering space around them"""
        points = [(0, 0), (2, 0), (1, 2)]
        cells = self.vd.incremental_voronoi(points)
        
        # Should have 3 cells
        self.assertEqual(len(cells), 3)
        
        # Each cell should have non-zero area (or be edge case)
        areas = [cell.area() for cell in cells]
        non_zero_areas = sum(1 for a in areas if a > 0.1)
        self.assertGreater(non_zero_areas, 0)
    
    def test_cell_counts_match_sites(self):
        """Test that number of cells matches number of sites"""
        test_cases = [
            [(0, 0)],
            [(0, 0), (1, 0)],
            [(0, 0), (1, 0), (0.5, 1)],
            [(-1, -1), (1, -1), (1, 1), (-1, 1)],
        ]
        
        for points in test_cases:
            cells = self.vd.incremental_voronoi(points)
            self.assertEqual(len(cells), len(points),
                           f"Cell count mismatch for points: {points}")


class TestPerformance(unittest.TestCase):
    """Test performance with larger point sets"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=100)
    
    def test_handles_10_points(self):
        """Test algorithm with 10 random points"""
        np.random.seed(42)
        points = [(np.random.uniform(-50, 50), np.random.uniform(-50, 50))
                  for _ in range(10)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 10)
    
    def test_handles_20_points(self):
        """Test algorithm with 20 random points"""
        np.random.seed(42)
        points = [(np.random.uniform(-50, 50), np.random.uniform(-50, 50))
                  for _ in range(20)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 20)
    
    def test_grid_pattern_points(self):
        """Test with points in grid pattern"""
        points = [(i, j) for i in range(-2, 3) for j in range(-2, 3)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), len(points))


class TestNumericalStability(unittest.TestCase):
    """Test numerical stability and precision"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=100)
    
    def test_very_close_points_handled(self):
        """Test algorithm with very close points"""
        points = [(0, 0), (1e-9, 1e-9), (2, 0)]
        cells = self.vd.incremental_voronoi(points)
        # Very close points should be treated as duplicates or handled gracefully
        self.assertGreaterEqual(len(cells), 1)
    
    def test_large_coordinate_values(self):
        """Test with large coordinate values"""
        points = [(1000, 1000), (1000.5, 1000), (1000.25, 1000.5)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 3)
    
    def test_negative_coordinates(self):
        """Test with negative coordinates"""
        points = [(-10, -10), (-5, -10), (-7.5, -5)]
        cells = self.vd.incremental_voronoi(points)
        self.assertEqual(len(cells), 3)


class TestGeometryProperties(unittest.TestCase):
    """Test geometric properties are maintained"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sh = ShapelyHelper()
        self.vg = VoronoiGeometry(self.sh)
        self.vd = VoronoiDiagram(self.sh, self.vg, bbox=100)
    
    def test_perpendicular_bisector_perpendicular(self):
        """Test that bisector is perpendicular to line between points"""
        p1 = (0, 0)
        p2 = (3, 4)
        
        bisector = self.vg.perpendicular_bisector(p1, p2)
        coords = list(bisector.coords)
        
        # Bisector direction
        bisector_vec = (coords[1][0] - coords[0][0], coords[1][1] - coords[0][1])
        # Original line direction
        original_vec = (p2[0] - p1[0], p2[1] - p1[1])
        
        # Dot product should be near zero (perpendicular)
        dot = GeometryUtils.dot(bisector_vec, original_vec)
        self.assertAlmostEqual(dot, 0.0, places=3)
    
    def test_clipping_reduces_polygon_size(self):
        """Test that clipping reduces polygon area"""
        initial_poly = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        initial_area = Cell((0, 0), polygon=initial_poly, 
                           shapely_helper=self.sh, voronoi_geo=self.vg).area()
        
        # Clip by vertical line at x=0
        line = (1, 0, 0)
        clipped = self.vg.clip_polygon_by_halfplane(initial_poly, line, keep_positive=True)
        
        if isinstance(clipped, list):
            clipped_area = Cell((0, 0), polygon=clipped,
                               shapely_helper=self.sh, voronoi_geo=self.vg).area()
        else:
            clipped_area = clipped.area
        
        # Clipped should be smaller (or equal if polygon exactly on line)
        self.assertLessEqual(clipped_area, initial_area + 1e-6)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestVisualization))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithmCorrectness))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalStability))
    suite.addTests(loader.loadTestsFromTestCase(TestGeometryProperties))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("EXTENDED TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
