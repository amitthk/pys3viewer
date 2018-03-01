class BucketMetaInfo:
    """Information about Bucket Object obtained from list_objects_v2
    https://boto3.readthedocs.io/en/stable/reference/services/s3.html#S3.Client.list_objects_v2
    """
    def __init__(self, Key = None, LastModified = None, ETag = None, Size = None, StorageClass = None, Owner = None):
        self.Key = Key
        self.LastModified = LastModified
        self.ETag = ETag
        self.Size = Size
        self.StorageClass = StorageClass
        self.Owner = Owner
