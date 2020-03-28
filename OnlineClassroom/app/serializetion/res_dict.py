#coding=utf-8

import json
from OnlineClassroom.app.err.BindValidateErr import *


# 通用父类返回
def commen_res(code,msg,data):
    return {
                "code":code,
                "msg":msg,
                "data":data
            }

# 通用成功返回 (需要自定义msg和data)
def commen_success_res(msg,data):
    res_item = commen_res(successCode,msg,data)
    return res_item


# 注册成功返回
def registry_success_res():
    res_item = commen_res(successCode,registry_msg,None)
    return res_item


# 账号已存在返回
def registry_account_existence_res(msg):
    if len(msg) == 0:
        msg = existence_msg
    res_item = commen_res(existence_code,msg,None)
    return res_item



# bind 表单数据异常      返回json
def BindValidateErr(msg):
    if len(msg) == 0:
        msg = from_err_msg
    res_item = commen_res(form_err_code,msg,None)
    return json.dumps(res_item)




# 密码错误
def pswd_check_err(msg):
    if len(msg) == 0:
        msg = pswd_err_msg
    res_item = commen_res(pswd_err_code,msg,None)
    return res_item


# 修改信息异常
def modify_err(msg):
    if len(msg) == 0:
        msg = modify_msg
    res_item = commen_res(modify_code,msg,None)
    return res_item


# 添加信息异常
def add_err(msg):
    if len(msg) == 0:
        msg = add_msg
    res_item = commen_res(add_code,msg,None)
    return res_item

# 删除信息异常
def del_err(msg):
    if len(msg) == 0:
        msg = del_msg
    res_item = commen_res(del_code,msg,None)
    return res_item

# token异常
def token_err(msg):
    if len(msg) == 0:
        msg = token_msg
    res_item = commen_res(token_code,msg,None)
    return res_item

# 身份异常
def identity_err(msg):
    if len(msg) == 0:
        msg = identity_msg
    res_item = commen_res(identity_code,msg,None)
    return res_item

# 购买异常
def shop_err(msg):
    if len(msg) == 0:
        msg = shop_msg
    res_item = commen_res(shop_code,msg,None)
    return res_item

# 查询异常
def query_err(msg):
    if len(msg) == 0:
        msg = query_msg
    res_item = commen_res(query_code,msg,None)
    return res_item


# 数值异常
def value_err(msg):
    if len(msg) == 0:
        msg = value_msg
    res_item = commen_res(value_code,msg,None)
    return res_item