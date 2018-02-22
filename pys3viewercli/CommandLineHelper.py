from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager


class CommandLineHelper:
    """Helper function used by Command Line interface to generate Readable output."""
    def __init__(self):
        super()

    @staticmethod
    def list_all_files_in_all_buckets_for_user(access_key_id, secret_access_key):
        """Instance method used to set credentials and list s3 bucket details using pys3viewer module."""
        return_string = ''
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        for bucket_name in buckets_for_user:
            return_string += '\n + ' + bucket_name
            for filename in bucket_manager.get_files_in_bucket(bucket_name):
                return_string += '\n -> ' + filename
        return return_string

    @staticmethod
    def list_bucket_info_for_user(access_key_id, secret_access_key):
        """Instance method used to set credentials and list s3 bucket details using pys3viewer module."""
        return_string = ''
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        for bucket_name in buckets_for_user:
            return_string += '\n + ' + bucket_name
            bucket_info = bucket_manager.get_bucket_statistics(bucket_name)
            return_string += '\n -> ' + str(bucket_info)
        return return_string
