from pys3viewer import MapReduceProvider


class EMRProvider(MapReduceProvider):
    def getbucketlist(self, user_credentials):
        print("EMR Fetch buckets list")

    def getfileslist(self, s3_bucket, user_credentials):
        print("EMR Fetch files list")
