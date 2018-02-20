from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager


class CommandLineHelper:
    def __init__(self):
        super()

    def build_user_session(self, access_key_id, secret_access_key):
        rtrnstr = ''
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        bucketsforuser = bucket_manager.get_buckets_for_user()
        for bucketname in bucketsforuser:
            rtrnstr += '\n +' + bucketname;
            for filename in bucket_manager.get_files_in_bucket(bucketname):
                rtrnstr += '\n -> ' + filename;
        return rtrnstr;
