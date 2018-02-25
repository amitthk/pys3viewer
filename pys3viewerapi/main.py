from flask import Flask, request
from flask_restful import Resource, Api
from flask import request, jsonify
import json
from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager
from pys3viewerapi.validator import validate
from flask.ext.cors import CORS

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
cors = CORS(app)
api = Api(app)



class BucketList(Resource):
    """
    API Class to list the s3 buckets for user
    """
    def post(self):
        """
        Simple API Method accessible over http://<server_ip>:<port>/buckets/<access_key_id>/<secret_access_key>

        Args:
        access_key_id: AWS access_key_id used to access the s3 buckets for a user
        secret_access_key: AWS secret_access_key used to access the s3 bucket for user

        Returns:
             A Dictionary of bucket names as key and corresponding details as values
        """
        try:
            form = validate()
            access_key_id = form['access_key_id']
            secret_access_key = form['secret_access_key']
            if (access_key_id is None) or (secret_access_key is None):
                error_result = {'data': [
                    {'error': 'Validation error. The data supplied is null or request is not in json format.'}]}
                return error_result
            else:
                result = self.handle_bucket_request(access_key_id, secret_access_key)
                return jsonify(result)
        except Exception as e:
            error_result = {'data': [{'error': str(e)}]}
            return jsonify(error_result)

    def handle_bucket_request(self, access_key_id, secret_access_key):
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_dictionary = {}
        for bucket_name in buckets_for_user:
            bucket_info = [str(bucket_manager.get_bucket_statistics(bucket_name))]
            bucket_dictionary.update({bucket_name: bucket_info})
        result = {'data': [bucket_dictionary]}
        return result

class BucketObjects(Resource):
    """
    API Class to list the s3 buckets for user
    """
    def post(self):
        """
        Simple API Method accessible over http://<server_ip>:<port>/bucketobjects/<access_key_id>/<secret_access_key>

        Args:
        access_key_id: AWS access_key_id used to access the s3 buckets for a user
        secret_access_key: AWS secret_access_key used to access the s3 bucket for user

        Returns:
             A Dictionary of bucket names as key and corresponding details as values
        """
        try:
            form = validate()
            access_key_id = form['access_key_id']
            secret_access_key = form['secret_access_key']
            if (access_key_id is None) or (secret_access_key is None):
                error_result = {'data': [{'error': 'Validation error. The data supplied is null or request is not in json format.'}]}
                return jsonify(error_result)
            else:
                result = self.handle_bucket_objects_request(access_key_id, secret_access_key)
                return jsonify(result)
        except Exception as e:
            error_result = {
                'data': [{'error': str(e)}]}
            return jsonify(error_result)

    def handle_bucket_objects_request(self, access_key_id, secret_access_key):
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_dictionary = {}
        for bucket_name in buckets_for_user:
            bucket_objects = [json.dumps(bucket_manager.get_files_in_bucket(bucket_name))]
            bucket_dictionary.update({bucket_name: bucket_objects})
        result = {'data': [bucket_dictionary]}
        return result


api.add_resource(BucketList, '/buckets')
api.add_resource(BucketObjects, '/bucketobjects')

if __name__ == '__main__':
    app.run(port=8081)
