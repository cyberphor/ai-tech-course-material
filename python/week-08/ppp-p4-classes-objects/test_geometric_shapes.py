"""Module providing test case class and methods"""

import unittest
from geometric_shapes import Circle, ComplexShape, Ellipse, GeometricShape, Square, Rectangle
from utils import InvalidArgumentError

class TestGeometricShape(unittest.TestCase):
    """Test class for GeometricShape class"""
    def setUp(self):
        self.geometric_shape = GeometricShape("Square")

    def test_get_name(self):
        self.assertEqual(self.geometric_shape.get_name(), "Square")

    def test_non_empty_string(self):
        with self.assertRaises(InvalidArgumentError):
            self.geometric_shape.set_name("")

    def test_positive_number(self):
        with self.assertRaises(InvalidArgumentError):
            self.geometric_shape.set_name(5)

class TestCircleClass(unittest.TestCase):
    """Test class for Circle class"""
    def setUp(self):
        self.circle = Circle(10)

    def test_get_name(self):
        """Test method for circle get name method"""
        self.assertEqual(self.circle.get_name(), "Circle")

    def test_geometric_shape_name(self):
        """Test method for circle name attribute"""
        self.assertEqual(self.circle._GeometricShape__name, "Circle")

    def test_get_radius(self):
        """Test method for circle get_radius method"""
        self.assertEqual(self.circle.get_radius(), 10)

    def test_set_radius(self):
        """Test method for circle set_radius method"""
        self.circle.set_radius(20)
        self.assertEqual(self.circle.get_radius(), 20)
    
    def test_get_semi_major_axis(self):
        """Test method for circle get_semi_major_axis method"""
        self.assertEqual(self.circle.get_semi_major_axis(), 10)

    def test_get_semi_minor_axis(self):
        """Test method for circle get_semi_minor_axis method"""
        self.assertEqual(self.circle.get_semi_minor_axis(), 10)

    def test_get_perimeter(self):
        """Test method for circle perimeter"""
        self.circle.set_radius(20)
        self.assertEqual(self.circle.get_perimeter(), 125.66370614359172)

    def test_get_area(self):
        """Test method for circle area"""
        self.circle.set_radius(20)
        self.assertEqual(self.circle.get_area(), 1256.6370614359173)

class TestEllipseClass(unittest.TestCase):
    """Test class for Ellipse class"""
    def setUp(self):
        self.ellipse = Ellipse(5, 10)

    def test_get_semi_major_axis(self):
        self.assertEqual(self.ellipse.get_semi_major_axis(), 5)

    def test_get_semi_minor_axis(self):
        self.assertEqual(self.ellipse.get_semi_minor_axis(), 10)

    def test_positive_semi_major_axis(self):
        with self.assertRaises(InvalidArgumentError):
            self.ellipse.set_semi_major_axis(-5)

    def test_positive_semi_minor_axis(self):
        with self.assertRaises(InvalidArgumentError):
            self.ellipse.set_semi_major_axis(-10)

class TestComplexShape(unittest.TestCase):
    """Test class for ComplexShape class"""

    def setUp(self):
        base = Ellipse(20, 10)
        hole1 = Square(5)
        hole2 = Circle(3)
        hole3 = Rectangle(5, 3)
        self.complex_shape = ComplexShape(base, [hole1, hole2, hole3])

    def test_get_name(self):
        """Test method for get_name method"""
        self.assertEqual(self.complex_shape.get_name(), "ComplexShape")

    def test_get_base(self):
        """Test method for get_base method"""
        self.assertTrue(isinstance(self.complex_shape.get_base(), Ellipse))

    def test_get_holes(self):
        """Test method for get_holes method"""
        holes = self.complex_shape.get_holes()
        self.assertTrue(isinstance(holes, list))
        for hole in holes:
            self.assertTrue(isinstance(hole, GeometricShape))

    def test_set_base(self):
        """Test method for set_base method"""
        self.complex_shape.set_base(Rectangle(20, 20))
        self.assertTrue(isinstance(self.complex_shape.get_base(), Rectangle))
    
    def test_set_holes(self):
        """Test method for set_holes method"""
        self.complex_shape.set_holes([])
        holes = self.complex_shape.get_holes()
        self.assertTrue(isinstance(holes, list))
        self.assertEqual(len(holes), 0)

    def test_add_hole(self):
        """Test method for add_hole method"""
        self.complex_shape.add_hole(Circle(3))
        self.assertTrue(self.complex_shape.get_holes(), ComplexShape(Ellipse, [Square, Circle, Rectangle, Circle]))

    def test_remove_hole(self):
        """Test method for remove_hole method"""
        hole = self.complex_shape.get_holes()[2]
        self.complex_shape.remove_hole(hole)
        self.assertTrue(self.complex_shape.get_holes(), ComplexShape(Ellipse, [Square, Circle]))

    def test_get_area(self):
        """Test method for get_area method"""
        self.assertEqual(self.complex_shape.get_area(), 560.0441968356505)

if __name__ == "__main__":
    unittest.main()