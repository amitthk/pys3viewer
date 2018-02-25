class BucketDetailsModel:
    def __init__(self, bucket_name=None):
        if bucket_name:
            self.bucket_name = bucket_name
            self.file_paths = []

    def serialize(self):
        return {
            'bucket_name': self.bucket_name,
            'file_paths': [file_path for file_path in self.file_paths]
        }
