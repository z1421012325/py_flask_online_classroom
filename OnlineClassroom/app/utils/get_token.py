#coding=utf-8


import jwt,time
from flask import current_app,request




# 默认盐值
default_secret_key = "123456789"
# 默认算法
default_algorithm = 'HS256'
# 过期时间
exp_time_unix = 86400 * 30


# 在当前app中取得配置
def get_secret_key():
    SECRET_KEY = ""
    try:
        SECRET_KEY = current_app.config["SECRET_KEY"]
        if len(SECRET_KEY) == 0:
            SECRET_KEY = default_secret_key
    except Exception as e:
        SECRET_KEY = default_secret_key
    return SECRET_KEY

# 从http请求的header中得到token
def requst_get_token():
    token = request.headers.get("Authorization")
    return token


def create_token(aid):
    key = get_secret_key()

    payload = {
        "iat":int(time.time()),
        "exp":int(time.time()) + exp_time_unix,
        "aid":aid
    }

    token = jwt.encode(payload,key, algorithm=default_algorithm)
    return str(token,"utf-8")


def check_token(token):
    key = get_secret_key()

    payload = jwt.decode(token, key, algorithm=[default_algorithm])

    if int(time.time()) < int(payload["exp"]):
        return True,int(payload["aid"])
    return False, ""



def create_admin_token(aid,usename,r_id):
    key = get_secret_key()

    payload = {
        "iat":int(time.time()),
        "exp":int(time.time()) + exp_time_unix,
        "data":{
            "aid":aid,
            "username":usename,
            "r_id":r_id
        }
    }

    token = jwt.encode(payload,key, algorithm=default_algorithm)
    return str(token,"utf-8")

def check_admin_token(token):
    key = get_secret_key()

    payload = jwt.decode(token, key, algorithm=[default_algorithm])

    if int(time.time()) < int(payload["exp"]):
        print("\n\n  {}\n\n".format(payload["data"]))
        return True,eval(str(payload["data"]))
    return False, ""

if __name__ == '__main__':
    token = create_token(11111)
    ok,aid = check_token(token)
    if ok:
        print(aid)
    else:
        print("None")