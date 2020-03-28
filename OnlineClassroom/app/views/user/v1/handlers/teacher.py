#coding=utf-8

from flask import Blueprint,jsonify,url_for

from OnlineClassroom.app.models.account import *
from OnlineClassroom.app.models.money import *
from OnlineClassroom.app.models.extracts import *

from OnlineClassroom.app.forms.teacher_forms import *
from OnlineClassroom.app.forms.paginate_form import *

from OnlineClassroom.app.serializetion.res_dict import *

from OnlineClassroom.app.utils.get_token import *

teacher = Blueprint("teacher_api_v1",__name__)


# @teacher.before_request
# def filter_is_token():
#     list_not_check_token_router = [
#         url_for("registry"),
#         url_for("teacher_all"),
#     ]
#
#     for p in list_not_check_token_router:
#         print("url_for :> ",p)
#         if p in request.path:
#             return None
#
#     token = requst_get_token()
#     ok, aid = check_token(token)
#     if ok:
#         return None
#     return jsonify(token_err(""))


# 老师注册

@teacher.route("registry",methods=["POST"])
def registry():

    form = registry_form()
    if not form.validate_for_api():
        return form.bindErr

    u = Account(nickname=form.nickname.data,username=form.username.data,pswd=form.pswd.data,info=form.info.data)
    if not u.registryTeacherAccount():
        return jsonify(registry_account_existence_res(""))

    return jsonify(registry_success_res())


# 展示所含有的老师
@teacher.route("/all",methods=["GET"])
def teacher_all():

    form = page_form()

    u = Account()
    items = u.query_Teachers(form.page.data,form.number.data)

    return jsonify(commen_success_res("",items))


# 查看课程被购买记录(老师)
@teacher.route("/show/curriculum/record",methods=["GET"])
def show_teacher_curriculum_record():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    c = Curriculums(aid=aid)
    items = c.get_purchase_records(page=request.args.get("page",1),number=request.args.get("number",10))

    return jsonify(commen_success_res("",items))


# 查看拥有金额(老师)
@teacher.route("/have/money",methods=["GET"])
def have_money():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    m = Money(aid=aid)
    item = {
        "current_money":str(m.get_user_money())
    }

    return jsonify(commen_success_res("",item))


# 提成金额(老师)  zfb
@teacher.route("/extract/money",methods=["POST"])
def extract_money():

    form = extract_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    """
        提成逻辑
            默认zfb提成,根据分成,提取0.05
                例 提取100 视频平台收手续费0.05 为 5,用户到手为 95
            前端页面连接支付宝接口验证是否为支付宝账号,验证成功则把支付宝返回的数据提交至该接口..
            由该接口服务调用支付宝转账服务,保存数据为暂时未完成转账交易状态 
            新增一个转账确认接口,接受支付宝转账交易情况并将转账交易状态更改为完成转账
    """


    m = Money(aid=aid)  # 查询该账户金额
    _money = m.get_user_money()

    if _money == None or float(_money) == 0.00:
        m.is_query_is_null_new_account()
        return jsonify(value_err("账户金额为0"))

    if float(form.money.data) > float(_money):
        return jsonify(value_err("提取金额超过拥有金额"))

    e = Extracts()

    divide = float(form.money.data) * float(e.money_divide)
    actual = float(form.money.data) - float(divide)

    e.new_extract(aid=aid,t_money=divide,actual_money=actual)
    uuid_number = e.get_number()
    """
        uuid_number 唯一单号,确定转账是否完成凭证
    """

    if not e.save(form.money.data):
        return jsonify(modify_err("转账交易失败"))

    """
        这里对第三方平台(zfb,wx)接口进行转账交易
        转账如果失败也会把uuid_number转递过来
        根据uuid_number去转账数据库查询得到转账失败的金额,进行原路返回
    """

    item = {
        "number":uuid_number,
        "status":e.status_not_complete,
    }

    return jsonify(commen_success_res("",item))


# 提成记录(老师)
@teacher.route("/extract/record",methods=["GET"])
def extract_record():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    ex = Extracts(aid=aid)
    items = ex.query_user_extracts(page=request.args.get("page",1),number=request.args.get("number",10))

    return jsonify(commen_success_res("",items))