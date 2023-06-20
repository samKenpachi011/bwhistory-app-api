"""
Sample tests
"""
from django.test import SimpleTestCase
from app import sample_cal_test


class SampleCalTests(SimpleTestCase):
    """A simple calculation class"""

    def test_add_numbers(self):
        """Test adding numbers together"""
        res = sample_cal_test.add(2, 3)
        self.assertEqual(res, 5)

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = sample_cal_test.subtract(5, 2)
        self.assertEqual(res, 3)
