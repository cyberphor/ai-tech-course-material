"""Module providing test case class and methods"""

import unittest
from utils import InvalidArgumentError, validate_positive_number, validate_non_empty_string

class TestUtilsModule(unittest.TestCase):
    """Test class for utils module"""

    def test_validate_positive_number(self):
        """Test method for validate_positive_number function"""
        self.assertEqual(validate_positive_number(5), None)

    def test_validate_non_empty_string(self):
        """Test method for validate_non_empty_string function"""
        self.assertEqual(validate_non_empty_string("Hello"), None)
        with self.assertRaises(InvalidArgumentError):
            validate_non_empty_string("")
            validate_non_empty_string(5)

if __name__ == "__main__":
    unittest.main()