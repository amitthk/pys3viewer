from boto3.session import Session


class CredentialManager:
    def __init__(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session = Session(aws_access_key_id=access_key_id,
                               aws_secret_access_key=secret_access_key)