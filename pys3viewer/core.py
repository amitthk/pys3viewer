# -*- coding: utf-8 -*-
from . import helpers

def build_user_session(username, secret_access_key):
    bucketstforuser = helpers.get_buckets_for_user(username);
    rtrnstr = 's3buckets for user {0}'.format(username)
    for bucketname in bucketstforuser:
        rtrnstr += '\n ' + bucketname;
        for filename in helpers.get_files_in_bucket(bucketname):
            rtrnstr += '\n '+filename;
    return rtrnstr;


def get_all_files_in_bucket():
    """Fetch all the files for bucket..."""
    username = input('Enter username:');
    print(build_user_session(username, ''));
