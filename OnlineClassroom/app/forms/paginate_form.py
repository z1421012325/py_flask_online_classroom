# coding=utf-8

from .RequestBaseForm import RequestBaseForm
from wtforms import IntegerField
from wtforms.validators import DataRequired,Length




class page_form(RequestBaseForm):
    page = IntegerField("page",validators=[])
    number = IntegerField("number",validators=[])

