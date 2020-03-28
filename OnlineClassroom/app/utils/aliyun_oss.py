# coding=utf-8


from oss2.api import *
from oss2.auth import *

from flask import current_app


def get_oss_auth_sigi():
    # access_key_id, access_key_secret
    access_key_id = current_app.config["ACCESS_KEY_ID"]
    access_key_secret = current_app.config["ACCESS_KEY_SECRET"]
    auth = AuthV2(access_key_id, access_key_secret)
    return auth

def get_oss_bucket(filename,input_time=60*60):
    auth = get_oss_auth_sigi()

    # endpoint, bucket_name
    # endpoint 假设为 http://oss-cn-hangzhou.aliyuncs.com
    # bucket_name 为存储空间名
    endpoint = current_app.config["ENDPOINT"]
    bucket_name = current_app.config["BUCKET_NAME"]

    bucket = Bucket(auth=auth,endpoint=endpoint,bucket_name=bucket_name)
    put_url = bucket.sign_url("PUT",filename,input_time)
    get_url = bucket.sign_url("GET", filename, input_time)


    di = {
        "get":get_url,
        "put":put_url
    }

    return di



def get_img_oss_url(filename,input_time=60*60):
    auth = get_oss_auth_sigi()

    endpoint = current_app.config["ENDPOINT"]
    bucket_name = current_app.config["BUCKET_NAME"]

    bucket = Bucket(auth=auth, endpoint=endpoint, bucket_name=bucket_name)
    get_url = bucket.sign_url("GET", filename, input_time)

    return get_url


if __name__ == '__main__':
    get_oss_bucket("123.jpg")