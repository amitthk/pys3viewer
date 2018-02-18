from boto3.session import Session

class s3helper():

    session = None;

    def get_files_in_bucket(self, bucketname):
        """All the files a bucket."""
        s3 = self.session.resource('s3')
        this_bucket = s3.Bucket(bucketname)
        lstfiles= [s3file.key for s3file in this_bucket.objects.all()];
        return lstfiles;

    def get_buckets_for_user(self, access_key_id, secret_access_key):
        """All the buckets for a user."""
        self.session = Session(aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)
        s3 = self.session.resource('s3')
        bucket_list = [bucket.name for bucket in s3.buckets.all()]

        return bucket_list;