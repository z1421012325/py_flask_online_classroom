# coding=utf-8

from .RequestBaseForm import RequestBaseForm
from wtforms import StringField,PasswordField,IntegerField,FloatField
from wtforms.validators import DataRequired,Length


# 注册表单
class registry_form(RequestBaseForm):
    nickname = StringField("nickname",validators=[DataRequired(),Length(min=2,max=20)])
    username = StringField("username",validators=[DataRequired(),Length(min=2,max=20)])
    pswd = PasswordField("pswd",validators=[DataRequired(),Length(min=8,max=50)])
    info = StringField("info")




# 提现表单
class extract_form(RequestBaseForm):
    money = FloatField("money",validators=[DataRequired()])
    account = StringField("account",validators=[DataRequired()])        # 假设只支持支付宝
