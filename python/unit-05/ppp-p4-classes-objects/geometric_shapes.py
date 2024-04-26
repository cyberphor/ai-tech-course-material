"""Module for geometric shapes"""

from math import pi, sqrt
from utils import validate_positive_number, validate_non_empty_string


class GeometricShape:
    """Geometric shape class"""

    def __init__(self, name):
        self.set_name(name)

    def set_name(self, name):
        """Setter method for geometric shape name"""
        if validate_non_empty_string(name) == None:
            self.__name = name

    def get_name(self):
        """Getter method for geometric shape name"""
        return self.__name

    def __repr__(self):
        """Representation method for GeometricShape class"""
        return f"GeometricShape(name={self.get_name()})"

    def __eq__(self, other):
        """Equals method for GeometricShape class"""
        if isinstance(other, GeometricShape):
            if self.get_name() == other.get_name():
                return True
        return False


class Rectangle(GeometricShape):
    """Rectangle class"""

    def __init__(self, length, width):
        super().__init__("Rectangle")
        self.set_length(length)
        self.set_width(width)

    def set_length(self, length):
        """Setter method for length of rectangle"""
        if validate_positive_number(length) is None:
            self.__length = length

    def get_length(self):
        """Getter method for length of rectangle"""
        return self.__length

    def set_width(self, width):
        """Setter method for width of rectangle"""
        if validate_positive_number(width) is None:
            self.__width = width

    def get_width(self):
        """Getter method for width of rectangle"""
        return self.__width

    def get_perimeter(self):
        """Getter method for perimeter of rectangle"""
        return 2 * self.get_length() + 2 * self.get_width()

    def get_area(self):
        """Getter method for area of rectangle"""
        return self.get_length() * self.get_width()

    def __repr__(self):
        return f"Rectangle(a={self.get_length()}, b={self.get_width()})"

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            if other.get_length() == self.get_length():
                if other.get_width() == self.get_width():
                    return True
        return False


class Ellipse(GeometricShape):
    """Ellipse class"""

    def __init__(self, semi_major_axis, semi_minor_axis):
        super().__init__("Ellipse")
        self.set_semi_major_axis(semi_major_axis)
        self.set_semi_minor_axis(semi_minor_axis)

    def set_semi_major_axis(self, semi_major_axis):
        """Setter method for semi major axis of ellipse"""
        if validate_positive_number(semi_major_axis) is None:
            self.__semi_major_axis = semi_major_axis

    def get_semi_major_axis(self):
        """Getter method for semi major axis of ellipse"""
        return self.__semi_major_axis

    def set_semi_minor_axis(self, semi_minor_axis):
        """Setter method for semi minor axis of ellipse"""
        if validate_positive_number(semi_minor_axis) is None:
            self.__semi_minor_axis = semi_minor_axis

    def get_semi_minor_axis(self):
        """Getter method for semi minor axis of ellipse"""
        return self.__semi_minor_axis

    def get_perimeter(self):
        """Getter method for perimeter of ellipse"""
        return pi * (
            3 * (self.get_semi_major_axis() + self.get_semi_minor_axis())
            - sqrt(
                (3 * self.get_semi_major_axis() + self.get_semi_minor_axis())
                * (self.get_semi_major_axis() + 3 * self.get_semi_minor_axis())
            )
        )

    def get_area(self):
        """Getter method for area of ellipse"""
        return self.get_semi_major_axis() * self.get_semi_minor_axis() * pi

    def __repr__(self):
        return (
            f"Ellipse(r1={self.get_semi_major_axis()}, r2={self.get_semi_minor_axis()})"
        )

    def __eq__(self, other):
        if isinstance(other, Ellipse):
            if other.get_semi_major_axis() == self.get_semi_major_axis():
                if other.get_semi_minor_axis() == self.get_semi_minor_axis():
                    return True
        return False


class Square(Rectangle):
    """Square class"""

    def __init__(self, side):
        super().__init__(side, side)
        super().set_name("Square")

    def set_side(self, side):
        """Setter method for side of square"""
        if validate_positive_number(side) is None:
            super().set_length(side)
            super().set_width(side)

    def get_side(self):
        """Getter method for side of square"""
        return super().get_length()

    def __repr__(self):
        return f"Square(a={self.get_side()})"

    def __eq__(self, other):
        if isinstance(other, Square):
            if other.get_side() == self.get_side():
                return True
        return False


class Circle(Ellipse):
    """Circle class"""

    def __init__(self, radius):
        super().__init__(
            radius, radius
        )  # use parent init method to init major/minor axis
        super().set_name("Circle")  # use parent setter method to set name

    def set_radius(self, radius):
        """Setter method for radius of circle"""
        if validate_positive_number(radius) is None:
            super().set_semi_major_axis(radius)
            super().set_semi_minor_axis(radius)

    def get_radius(self):
        """Getter method for radius of circle"""
        return super().get_semi_major_axis()

    def __repr__(self):
        return f"Circle(r={self.get_radius()})"

    def __eq__(self, other):
        if isinstance(other, Circle):
            if other.get_radius() == self.get_radius():
                return True
        return False


class ComplexShape(GeometricShape):
    """ComplexShape class"""

    def __init__(self, base, holes):
        super().__init__("ComplexShape")
        self.set_base(base)
        self.set_holes(holes)

    def set_base(self, base: GeometricShape):
        """Setter method for base of ComplexShape"""
        self.__base = base

    def get_base(self):
        """Getter method for base of ComplexShape"""
        return self.__base

    def set_holes(self, holes: list[GeometricShape]):
        """Setter method for holes of ComplexShape"""
        self.__holes = holes

    def get_holes(self):
        """Getter method for holes of ComplexShape"""
        return self.__holes

    def add_hole(self, hole: GeometricShape):
        """Method for adding a hole to a ComplexShape"""
        self.__holes.append(hole)

    def remove_hole(self, hole):
        """Method for removing a hole from a ComplexShape"""
        for i in self.get_holes():
            if hole in self.get_holes():
                self.__holes.remove(hole)

    def get_area(self):
        """Getter method for area of a ComplexShape"""
        base_area = self.get_base().get_area()
        hole_areas = []
        for hole in self.get_holes():
            hole_areas.append(hole.get_area())
        return base_area - sum(hole_areas)

    def get_edge_length(self):
        """Getter method for edge_length of a ComplexShape"""
        base_edge_length = self.get_base().get_perimeter()
        hole_edge_lengths = []
        for hole in self.get_holes():
            hole_edge_lengths.append(hole.get_perimeter())
        return base_edge_length + sum(hole_edge_lengths)

    def __repr__(self):
        return f"ComplexShape({self.get_base().get_name()} with {len(self.get_holes())} holes)"
