from boto3.session import Session


class CredentialManager:
    """
    CredentialsManager class used to keep credentials & session for the user

    Args:
        access_key_id: AWS access_key_id used to access the s3 buckets for a user
        secret_access_key: AWS secret_access_key used to access the s3 bucket for user
    """
    def __init__(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session = Session(aws_access_key_id=access_key_id,
                               aws_secret_access_key=secret_access_key)