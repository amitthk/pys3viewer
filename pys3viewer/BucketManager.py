from .CredentialManager import CredentialManager
from .BucketInfo import BucketInfo


class BucketManager:
    def __init__(self, user_credentials: CredentialManager):
        self.credentials = user_credentials

    def get_buckets_for_user(self):
        """
        Lists All the buckets for a user.

        Args:
        user_credentials: CredentialManager

        Returns:
            List of all the buckets for the user
        """
        s3 = self.credentials.session.resource('s3')
        bucket_list = [bucket.name for bucket in s3.buckets.all()]

        return bucket_list;

    def get_bucket_statistics(self, bucket_name):
        """
        Fetches the bucket information

        :param
        bucket_name:

        :return:
        bucket_info of type BucketInfo
        """
        bucket_info = BucketInfo()
        bucket_info.bucket_name = bucket_name
        s3 = self.credentials.session.resource('s3')
        current_bucket = s3.Bucket(bucket_name)
        bucket_info.creation_date = current_bucket.creation_date

        for bucket_object in current_bucket.objects.all():
            bucket_info.total_size_of_files += bucket_object.size
            bucket_info.number_of_files += 1
            if (bucket_info.last_modified is None) or (bucket_object.last_modified > bucket_info.last_modified):
                bucket_info.last_modified = bucket_object.last_modified

        return bucket_info

    def get_bucket_statistics_v2(self, bucket_name, storageTypeFilter=None):
        """
        Fetches the bucket information

        :param
        bucket_name:

        :return:
        bucket_info of type BucketInfo
        """
        bucket_info = BucketInfo()
        bucket_info.bucket_name = bucket_name
        s3 = self.credentials.session.resource('s3')
        current_bucket = s3.Bucket(bucket_name)
        bucket_info.creation_date = current_bucket.creation_date
        #get_object_info = lambda obj: [int(obj['LastModified'].strftime('%s')), obj['Size'], obj['StorageClass']]

        for bucket_object in self.iterate_bucket_objects(bucket=bucket_name):
            if storageTypeFilter is None:
                bucket_info.total_size_of_files += int(bucket_object['Size'])
                _last_modified = bucket_object['LastModified']
                bucket_info.number_of_files += 1
                if (bucket_info.last_modified is None) or (_last_modified > bucket_info.last_modified):
                    bucket_info.last_modified = _last_modified
            elif storageTypeFilter is bucket_object['StorageClass']:
                bucket_info.total_size_of_files += int(bucket_object['Size'])
                _last_modified = bucket_object['LastModified']
                bucket_info.number_of_files += 1
                if (bucket_info.last_modified is None) or (_last_modified > bucket_info.last_modified):
                    bucket_info.last_modified = _last_modified


        return bucket_info

    def iterate_bucket_objects(self, bucket):
        """
        Generator that iterates over all objects in a given s3 bucket
        :param bucket: name of s3 bucket
        :return: dict of metadata for an object
        """
        client = self.credentials.session.client('s3')
        page_iterator = client.list_objects_v2(Bucket=bucket)
        if 'Contents' not in page_iterator:
            return []
        for item in page_iterator['Contents']:
            yield item


    def get_files_in_bucket(self, bucket_name):
        """Returns he list of objects within a bucket.

        Args:
            bucket_name: name of bucket
        Returns:
            list of all objects within bucket
        """
        s3 = self.credentials.session.resource('s3')
        this_bucket = s3.Bucket(bucket_name)
        list_of_files = [s3file.key for s3file in this_bucket.objects.all()];
        return list_of_files

    def get_files_in_bucket_v2(self, bucket_name):
        """Returns he list of objects within a bucket.

        Args:
            bucket_name: name of bucket
        Returns:
            list of all objects within bucket
        """
        list_of_files = [s3file['Key'] for s3file in self.iterate_bucket_objects(bucket=bucket_name)]
        return list_of_files
