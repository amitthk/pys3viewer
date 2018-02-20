from . import CredentialManager


class BucketManager:
    def __init__(self, user_credentials: CredentialManager):
        self.credentials = user_credentials

    def get_files_in_bucket(self, bucketname):
        """All the files a bucket."""
        s3 = self.credentials.session.resource('s3')
        this_bucket = s3.Bucket(bucketname)
        lstfiles = [s3file.key for s3file in this_bucket.objects.all()];
        return lstfiles;

    def get_buckets_for_user(self):
        """All the buckets for a user.
        :type user_credentials: CredentialManager
        """
        s3 = self.credentials.session.resource('s3')
        bucket_list = [bucket.name for bucket in s3.buckets.all()]

        return bucket_list;
