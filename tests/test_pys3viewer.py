# -*- coding: utf-8 -*-

from .context import pys3viewer
from django import VERSION


if VERSION >= (1, 7):
    import unittest
else:
    from django.utils import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def setUp(self):
        pass

    def test_buckets_for_a_user(self):
        username = input('Enter username:');
        access_key = input('Enter access key:');
        result = pys3viewer.get_all_files_in_bucket(username, access_key)
        print(result);
        self.assertIsNotNone(result)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
