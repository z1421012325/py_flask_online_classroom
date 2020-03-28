# coding=utf-8

from .RequestBaseForm import RequestBaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import DataRequired




class search_form(RequestBaseForm):
    key = StringField("key",validators=[])
    # order 默认1 为默认排序 2 为(购买)热门排序,3 为最新排序
    order = StringField("order",validators=[])
    page = IntegerField("page",validators=[])
    number = IntegerField("number",validators=[])


