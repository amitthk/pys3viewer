from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager


class CommandLineHelper:
    """Helper function used by Command Line interface to generate Readable output."""
    def __init__(self):
        super()

    @staticmethod
    def list_all_files_in_all_buckets_for_user(access_key_id, secret_access_key):
        """
        Instance method used to set credentials and list all the s3 buckets and its files accessible by a user

        Args:
            access_key_id: AWS access_key_id used to access the s3 buckets for a user
            secret_access_key: AWS secret_access_key used to access the s3 bucket for user

        Returns:
            String value representing the tree format structure of all the s3 buckets accessible by user

        """
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
        """
        Instance method used to set credentials and list all the s3 buckets and its files accessible by a user

        Args:
            access_key_id: AWS access_key_id used to access the s3 buckets for a user
            secret_access_key: AWS secret_access_key used to access the s3 bucket for user

        Returns:
            String value representing each s3 bucket and corresponding details for each bucket
        """
        return_string = ''
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        for bucket_name in buckets_for_user:
            return_string += '\n + ' + bucket_name
            bucket_info = bucket_manager.get_bucket_statistics(bucket_name)
            format_string = "\n   -> bucket_name : {0}, \n   -> creation_date : {1},"\
                            "\n   -> number_of_files : {2}, \n   -> total_size_of_files : {3},"\
                            "\n   -> last_modified : {4}"
            return_string += format_string.format(bucket_info.bucket_name, bucket_info.creation_date,
                                                  bucket_info.number_of_files, bucket_info.total_size_of_files, bucket_info.last_modified)

        return return_string
