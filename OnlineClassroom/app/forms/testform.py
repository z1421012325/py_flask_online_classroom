# coding=utf-8

from .RequestBaseForm import RequestBaseForm
from wtforms import StringField
from wtforms.validators import DataRequired,Length


# test
class Test_form(RequestBaseForm):
    username = StringField("username",validators=[DataRequired(),Length(min=2,max=20)])
