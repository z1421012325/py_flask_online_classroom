# coding=utf-8

from .RequestBaseForm import RequestBaseForm
from wtforms import StringField,PasswordField,IntegerField
from wtforms.validators import DataRequired,Length



# 注册表单
class registry_form(RequestBaseForm):
    nickname = StringField("nickname",validators=[DataRequired(),Length(min=2,max=20)])
    username = StringField("username",validators=[DataRequired(),Length(min=2,max=20)])
    pswd = PasswordField("pswd",validators=[DataRequired(),Length(min=8,max=50)])
    info = StringField("info")



# 登录表单
class login_form(RequestBaseForm):
    username = StringField("username",validators=[DataRequired(),Length(min=2,max=20)])
    pswd = PasswordField("pswd",validators=[DataRequired(),Length(min=8,max=50)])


# 修改账号信息
class modify_info_form(RequestBaseForm):
    nickname = StringField("nickname",validators=[DataRequired(),Length(min=2,max=20)])
    info = StringField("info")


# 修改账号密码
class modify_pswd_form(RequestBaseForm):
    old = StringField("old",validators=[DataRequired(),Length(min=8,max=50)])
    new = StringField("new", validators=[DataRequired(), Length(min=8, max=50)])



# 添加评论表单
class add_comment_form(RequestBaseForm):
    cid = IntegerField("cid", validators=[DataRequired()])
    comment = StringField("comment", validators=[DataRequired(), Length(min=1, max=1000)])
    number = IntegerField("number", validators=[])


# 删除评论表单
class del_comment_form(RequestBaseForm):
    id = IntegerField("id", validators=[DataRequired()])


# 保存用户头像
class save_user_portrait_form(RequestBaseForm):
    portrait = StringField("portrait", validators=[DataRequired()])