from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import json
from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager


app = Flask(__name__)
api = Api(app)


class BucketList(Resource):
    """
    API Class to list the s3 buckets for user
    """
    def get(self, access_key_id, secret_access_key):
        """
        Simple API Method accessible over http://<server_ip>:<port>/buckets/<access_key_id>/<secret_access_key>

        Args:
        access_key_id: AWS access_key_id used to access the s3 buckets for a user
        secret_access_key: AWS secret_access_key used to access the s3 bucket for user

        Returns:
             A Dictionary of bucket names as key and corresponding details as values
        """
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_dictionary = {}
        for bucket_name in buckets_for_user:
            bucket_info = [str(bucket_manager.get_bucket_statistics(bucket_name))]
            bucket_dictionary.update({bucket_name : bucket_info })
        result = {'data': [bucket_dictionary]}
        return jsonify(result)

class BucketObjects(Resource):
    """
    API Class to list the s3 buckets for user
    """
    def get(self, access_key_id, secret_access_key):
        """
        Simple API Method accessible over http://<server_ip>:<port>/buckets/<access_key_id>/<secret_access_key>

        Args:
        access_key_id: AWS access_key_id used to access the s3 buckets for a user
        secret_access_key: AWS secret_access_key used to access the s3 bucket for user

        Returns:
             A Dictionary of bucket names as key and corresponding details as values
        """
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_dictionary = {}
        for bucket_name in buckets_for_user:
            bucket_objects = [json.dumps(bucket_manager.get_files_in_bucket(bucket_name))]
            bucket_dictionary.update({bucket_name : bucket_objects })
        result = {'data': [bucket_dictionary]}
        return jsonify(result)


api.add_resource(BucketList, '/buckets/<access_key_id>/<secret_access_key>')
api.add_resource(BucketObjects, '/bucketobjects/<access_key_id>/<secret_access_key>')

if __name__ == '__main__':
    app.run(port=8081)
