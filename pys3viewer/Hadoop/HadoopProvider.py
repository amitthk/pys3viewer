from pys3viewer import MapReduceProvider


class HadoopProvider(MapReduceProvider):
    def getbucketlist(self, UserCredentials):
        print("Hadoop Fetch buckets list")
    def getfileslist(self, s3Bucket, UserCredentials):
        print("Hadoop Fetch files list")
