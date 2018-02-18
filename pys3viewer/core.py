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


def get_all_files_in_bucket(username, access_key):
    return build_user_session(username, access_key);
