# Object-Oriented Programming

## Training Objectives
1. Define a class with attributes and methods
2. Define a class with private attributes and setter/getter methods
3. Define a child class
4. Define a module
5. Define a class with attributes and methods that contain other classes
6. Initialize an object using a user-defined class
7. Define a class with `__repr__` and `__eq__` methods

## Setup
**Step 1.** Download the source code.
```bash
wget https://principlesofcomputing.blob.core.windows.net/ppp-p4-classes-objects/handout/sail2/ppp-p4-classes-objects.zip
unzip ppp-p4-classes-objects.zip
cd ppp-p4-classes-objects
```

**Step 2.** Setup a virtual environment. 
```bash
python -m venv p4-env
source p4-env/bin/activate
```

**Step 3.** Download dependencies. 
```
python -m pip install -r requirements.txt
```

## Testing
**Step 1.** Add the source code below into a file called `test_geometric_shapes.py`. Make sure it's in the same directory as the module you want to test. 
```python
"""Module providing test case class and methods"""
import unittest
from geometric_shapes import Circle

class TestCircleClass(unittest.TestCase):
    """Test class for circle class"""
    def setUp(self):
        self.circle = Circle(10)
    
    def test_get_radius(self):
        """Test method for circle get_radius method"""
        self.assertEqual(self.circle.get_radius(), 10)
    
    def test_set_radius(self):
        """Test method for circle set_radius method"""
        self.circle.set_radius(20)
        self.assertEqual(self.circle.get_radius(), 20)
    
    def test_get_name(self):
        """Test method for circle get name method"""
        self.assertEqual(self.circle.get_name(), "Circle")

    def test_geometric_shape_name(self):
        """Test method for circle name attribute"""
        self.assertEqual(self.circle._GeometricShape__name, "Circle")
    
    def test_get_semi_major_axis(self):
        """Test method for circle get semi_major_axis method"""
        self.assertEqual(self.circle.get_semi_major_axis(), 10)

    def test_get_semi_minor_axis(self):
        """Test method for circle get semi_minor_axis method"""
        self.assertEqual(self.circle.get_semi_major_axis(), 10)

    def test_get_perimeter(self):
        """Test method for circle perimeter"""
        self.circle.set_radius(20)
        self.assertEqual(self.circle.get_perimeter(), 125.66370614359172)

    def test_get_area(self):
        """Test method for circle area"""
        self.circle.set_radius(20)
        self.assertEqual(self.circle.get_area(), 1256.6370614359173)

if __name__ == "__main__":
    unittest.main()
```

**Step 2.** Run the Python Unit Tests module. 
```python
python -m unittest
```

An alternative to running all tests within the current directory is specifying the file-path. 
```bash
python test_geometric_shapes.py
```