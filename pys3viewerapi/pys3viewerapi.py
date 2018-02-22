from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
from pys3viewer.CredentialManager import CredentialManager
from pys3viewer.BucketManager import BucketManager


app = Flask(__name__)
api = Api(app)


class Bucket_List(Resource):

    def get(self, access_key_id, secret_access_key):
        user_credentials = CredentialManager(access_key_id, secret_access_key)
        bucket_manager = BucketManager(user_credentials)
        buckets_for_user = bucket_manager.get_buckets_for_user()
        bucket_dictionary = {}
        for bucket_name in buckets_for_user:
            bucket_info = [str(bucket_manager.get_bucket_statistics(bucket_name))]
            bucket_dictionary.update({bucket_name : bucket_info })
        result = {'data': [bucket_dictionary]}
        return jsonify(result)

api.add_resource(Bucket_List, '/buckets/<access_key_id>/<secret_access_key>')  # Route_3

if __name__ == '__main__':
    app.run(port=8081)
