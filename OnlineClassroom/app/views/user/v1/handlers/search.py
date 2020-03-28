#coding=utf-8

from flask import Blueprint,jsonify,request

from OnlineClassroom.app.models.curriculums import Curriculums
from OnlineClassroom.app.forms.search_forms import *

from OnlineClassroom.app.serializetion.res_dict import *

from OnlineClassroom.app.forms.search_forms import *

search = Blueprint("search_api_v1",__name__)

# todo 还有排序没做  分页

# search 搜索  时间排序,购买排序
@search.route("/search",methods=["GET"])
def search_curriculum():

    form = search_form()

    cc = Curriculums()
    items = cc.query_like_field_all(
                key=form.key.data,
                page=form.page.data,
                number=form.number.data,
                order=form.order.data
                                    )

    return jsonify(commen_success_res("",items))
