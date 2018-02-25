import sys
from flask import request
from flask_restful import reqparse

def validate():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('access_key_id', required=True)
    parser.add_argument('secret_access_key', required=True)
    args = parser.parse_args()
    return args
