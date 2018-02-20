# -*- coding: utf-8 -*-
from pys3viewercli.CommandLineHelper import CommandLineHelper

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
        access_key_id = input('Enter access_key_id:');
        secret_access_key = input('Enter secret_access_key:');
        command_line_helper = CommandLineHelper()
        result = command_line_helper.build_user_session(access_key_id, secret_access_key)
        print(result);
        self.assertIsNotNone(result)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
