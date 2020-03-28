# coding=utf-8

from flask import request
from wtforms import Form
from OnlineClassroom.app.serializetion.res_dict import BindValidateErr

# request data 基础验证器
class RequestBaseForm(Form):
    # 解析请求参数
    def __init__(self):

        req_mothod = request.method
        req_type = request.headers.get("Content-Type")
        if req_type ==None:
            req_type = "application/json"

        if req_mothod == "GET":
            data = request.args.to_dict()
            super(RequestBaseForm, self).__init__(data=data)

        # 解析非get请求的参数,如果是json则request.get_json()得到数据...
        if "application/json" in req_type and req_mothod not in "GET":
            data = request.get_json(silent=True)
            super(RequestBaseForm, self).__init__(data=data)

        elif "application/json" not in req_type and req_mothod not in "GET":
            # application/x-www-form-urlencoded    or    multipart/form-data
            data = request.form.to_dict()
            super(RequestBaseForm, self).__init__(data=data)

    # 对验证错误的参数抛出异常
    def validate_for_api(self):
        valid = super(RequestBaseForm, self).validate()
        if not valid:
            # 一个bind数据绑定错误返回方法,默认json序列化了
            self.BindErrToRes("field is not bind")
            return False
        return True


    # bind数据没有根据绑定的要求所返回的json数据
    bindErr = None
    def BindErrToRes(self,msg):
        self.bindErr = BindValidateErr(msg)

    def NoneErrToRes(self,msg):
        self.bindErr = BindValidateErr(msg)