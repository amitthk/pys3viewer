from flask import Flask, request
from flask_restful import Resource, Api
from flask import request, jsonify
import json
from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager
from pys3viewerapi.validator import validate
from pys3viewerapi.BucketDetailsModel import BucketDetailsModel
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
                bucket_list = self.handle_bucket_request(access_key_id, secret_access_key)
                result = [b.serialize() for b in bucket_list]
                return jsonify(result)
        except Exception as e:
            error_result = {'data': [{'error': str(e)}]}
            return jsonify(error_result)

    def handle_bucket_request(self, access_key_id, secret_access_key):
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_list = list()
        for bucket_name in buckets_for_user:
            bucket_info = bucket_manager.get_bucket_statistics_v2(bucket_name)
            bucket_list.append(bucket_info)
        return bucket_list

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
                bucket_list = self.handle_bucket_objects_request(access_key_id, secret_access_key)
                result = [b.serialize() for b in bucket_list]
                return jsonify(result)
        except Exception as e:
            error_result = {
                'data': [{'error': str(e)}]}
            return jsonify(error_result)

    def handle_bucket_objects_request(self, access_key_id, secret_access_key):
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_list = list()
        for bucket_name in buckets_for_user:
            bucket_object = BucketDetailsModel(bucket_name)
            bucket_object.file_paths = [str(f) for f in bucket_manager.get_files_in_bucket_v2(bucket_name)]
            bucket_list.append(bucket_object)
        return bucket_list


api.add_resource(BucketList, '/buckets')
api.add_resource(BucketObjects, '/bucketobjects')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
