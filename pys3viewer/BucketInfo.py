
class BucketInfo:
    """Model class for bucket information"""
    def __init__(self, bucket_name=None, creation_date=None, number_of_files=None, total_size_of_files=None, last_modified=None, storage_class=None):
        if bucket_name:
            self.bucket_name = bucket_name
        if creation_date:
            self.creation_date = creation_date
        if number_of_files:
            self.number_of_files = number_of_files
        else:
            self.number_of_files = 0
        if total_size_of_files:
            self.total_size_of_files = total_size_of_files
        else:
            self.total_size_of_files = 0
        self.last_modified = last_modified
        self.storage_class = storage_class

    def __str__(self):
        return "bucket_name: {0}, creation_date : {1}, number_of_files : {2}, total_size_of_files : {3}, last_modified : {1}".format(self.bucket_name, self.creation_date, self.number_of_files, self.total_size_of_files, self.last_modified)

    def serialize(self):
        return {
            'bucket_name': self.bucket_name,
            'creation_date': self.creation_date,
            'number_of_files': self.number_of_files,
            'total_size_of_files': self.total_size_of_files,
            'last_modified': self.last_modified
        }