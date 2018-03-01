class BucketObjectInfo:
    """Information about Bucket Object obtained from list_objects_v2
    http://boto3.readthedocs.io/en/latest/reference/services/s3.html#object
    """
    def __init__(self, accept_ranges=None, cache_control=None, content_disposition=None, content_encoding=None,
                 content_language=None, content_length=None, content_type=None, delete_marker=None, e_tag=None,
                 expiration=None, expires=None, last_modified=None, metadata=None, missing_meta=None, parts_count=None,
                 replication_status=None, request_charged=None, restore=None, server_side_encryption=None,
                 sse_customer_algorithm=None, sse_customer_key_md5=None, ssekms_key_id=None, storage_class=None,
                 version_id=None, website_redirect_location=None):
        self.accept_ranges = accept_ranges
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_language = content_language
        self.content_length = content_length
        self.content_type = content_type
        self.delete_marker = delete_marker
        self.e_tag = e_tag
        self.expiration = expiration
        self.expires = expires
        self.last_modified = last_modified
        self.metadata = metadata
        self.missing_meta = missing_meta
        self.parts_count = parts_count
        self.replication_status = replication_status
        self.request_charged = request_charged
        self.restore = restore
        self.server_side_encryption = server_side_encryption
        self.sse_customer_algorithm = sse_customer_algorithm
        self.sse_customer_key_md5 = sse_customer_key_md5
        self.ssekms_key_id = ssekms_key_id
        self.storage_class = storage_class
        self.version_id = version_id
        self.website_redirect_location = website_redirect_location
