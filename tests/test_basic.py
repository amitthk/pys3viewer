# -*- coding: utf-8 -*-

from .context import pys3viewer

from django import VERSION


if VERSION >= (1, 7):
    import unittest
else:
    from django.utils import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True


if __name__ == '__main__':
    unittest.main()