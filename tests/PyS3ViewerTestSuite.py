"""
Test suite for pys3viewer module and submodules

"""
from pys3viewercli.CommandLineHelper import CommandLineHelper
from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager
from django import VERSION


if VERSION >= (1, 7):
    import unittest
else:
    from django.utils import unittest


class PyS3ViewerTestSuite(unittest.TestCase):
    """Combined test cases."""

    def setUp(self):
        pass

    def test_buckets_for_a_user(self):
        access_key_id = input('Enter access_key_id:');
        secret_access_key = input('Enter secret_access_key:');
        return_string = ''
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        return_string = bucket_manager.get_buckets_for_user()
        print(return_string);
        self.assertIsNotNone(return_string)

    def test_all_files_in_bucket(self):
        access_key_id = input('Enter access_key_id:');
        secret_access_key = input('Enter secret_access_key:');
        return_string = ''
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        for bucket_name in buckets_for_user:
            return_string += '\n + ' + bucket_name
            for filename in bucket_manager.get_files_in_bucket(bucket_name):
                return_string += '\n -> ' + filename
        print(return_string);
        self.assertIsNotNone(return_string)

        def test_bucket_info_for_a_user(self):
            access_key_id = input('Enter access_key_id:');
            secret_access_key = input('Enter secret_access_key:');
            return_string = ''
            user_credentials = CredentialManager(access_key_id, secret_access_key)
            bucket_manager = BucketManager(user_credentials)
            buckets_for_user = bucket_manager.get_buckets_for_user()
            for bucket_name in buckets_for_user:
                return_string += '\n + ' + bucket_name
                for filename in bucket_manager.get_files_in_bucket(bucket_name):
                    return_string += '\n -> ' + filename
            print(return_string);
            self.assertIsNotNone(return_string)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
