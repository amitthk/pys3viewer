# -*- coding: utf-8 -*-

from .context import pys3viewer
from django import VERSION


if VERSION >= (1, 7):
    import unittest
else:
    from django.utils import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(pys3viewer.get_all_files_in_bucket())


if __name__ == '__main__':
    unittest.main()
