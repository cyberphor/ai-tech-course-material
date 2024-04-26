"""Module for variables"""

from geometric_shapes import Rectangle, Ellipse, Square, Circle, ComplexShape

rectangle = Rectangle(length=10, width=20)
ellipse = Ellipse(semi_major_axis=9, semi_minor_axis=7)
square = Square(side=4)
circle = Circle(radius=20)
complex_shape = ComplexShape(base=circle, holes=[rectangle, ellipse, square])
complex_shape_area = complex_shape.get_area()
complex_shape_edge_length = complex_shape.get_edge_length()
