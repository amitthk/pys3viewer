# -*- coding: utf-8 -*-
from . import helpers
from .classes.s3helper import s3helper


def build_user_session(access_key_id, secret_access_key):
    rtrnstr = ''
    s3h = s3helper()
    bucketstforuser = s3h.get_buckets_for_user(access_key_id, secret_access_key);
    for bucketname in bucketstforuser:
        rtrnstr += '\n +' + bucketname;
        for filename in s3h.get_files_in_bucket(bucketname):
            rtrnstr += '\n -> '+filename;
    return rtrnstr;


def get_all_files_in_bucket(access_key_id, secret_access_key):
    return build_user_session(access_key_id, secret_access_key);
