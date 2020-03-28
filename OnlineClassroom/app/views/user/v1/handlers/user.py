# coding=utf-8

from flask import Blueprint,jsonify,request,url_for
from OnlineClassroom.app.forms.user_forms import *
from OnlineClassroom.app.models.account import Account as account
from OnlineClassroom.app.models.shopping_carts import *

from OnlineClassroom.app.serializetion.res_dict import *
from OnlineClassroom.app.utils.get_token import check_token,create_token,requst_get_token

user = Blueprint('user_api_v1',__name__)

# @user.before_request
# def filter_is_token():
#
#     list_not_check_token_router = [
#         url_for("login"),
#         url_for("registry"),
#         url_for("get_user_info"),
#     ]
#
#     # not_filter = ["login", "registry", "register"]
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


# 登录
@user.route("login",methods=["POST"])
def login():

    form = login_form()
    if not form.validate_for_api():
        return jsonify(form.bindErr)

    u = account.query.filter(account.username==form.username.data).first()
    if not u.CheckPassword(form.pswd.data):
        return jsonify(pswd_check_err(""))

    #  返回token 塞入数据为用户id
    token = create_token(u.aid)

    item = {
        "username":u.username,
        "nickname":u.nickname,
        "token":token
    }

    return jsonify(commen_success_res("",item))

# 注册
@user.route("registry",methods=["POST"])
def registry():

    form = registry_form()
    if not form.validate_for_api():
        return jsonify(form.bindErr)

    u = account(form.nickname.data,form.username.data,form.pswd.data,form.info.data)

    if not u.registryStudentAccount():
        return jsonify(registry_account_existence_res(""))

    return jsonify(registry_success_res())

# 退出登录
@user.route("logout",methods=["POST"])
def logout():
    token = requst_get_token()
    print(token)
    return jsonify(commen_success_res("",""))


# 修改个人信息 (昵称,info)
@user.route("/modify/info",methods=["POST"])
def modify_user():

    form = modify_info_form()
    if not form.validate_for_api():
        return jsonify(form.bindErr)


    token = requst_get_token()
    ok,aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = account.query.filter(account.aid==int(aid)).first()
    if not u.modify_user_info(form.nickname.data,form.info.data):
        return jsonify(modify_err(""))

    return jsonify(commen_success_res("修改信息成功",""))


# 修改密码
@user.route("/modify/password",methods=["POST"])
def modify_user_password():

    form = modify_pswd_form()
    if not form.validate_for_api():
        return jsonify(form.bindErr)

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = account.query.filter(account.aid == int(aid)).first()

    if not u.modify_pswd(form.old.data,form.new.data):
        return jsonify(modify_err(""))

    return jsonify(commen_success_res("密码修改成功",""))






# 用户信息
@user.route("/info/<int:aid>",methods=["GET"])
def get_user_info(aid):

    u = account(aid=aid)
    item = u.get_aid_user_to_serializetion()

    return jsonify(commen_success_res("",item))




# 查看购买的视频
@user.route("/show/study",methods=["GET"])
def get_show_study():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    shop = ShoppingCarts(aid=aid)
    items = shop.get_purchase_curriculums(page=request.args.get("page",1),number=request.args.get("number",10))


    return jsonify(commen_success_res("",items))



# 发表评论
@user.route("/add/comment",methods=["POST"])
def add_comment():

    form = add_comment_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    comment = CurriculumComments(aid=aid,cid=form.cid.data,number=form.number.data,comment=form.comment.data)
    if not comment.save():
        return jsonify(add_err("该课程已经评论或者评论异常"))

    return jsonify(commen_success_res("评论添加成功",""))

# 查看发表的评论
@user.route("/see/comment",methods=["GET"])
def see_comment():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    comment = CurriculumComments(aid=aid)
    items = comment.query_user_comments(page=request.args.get("page",1),number=request.args.get("number",10))

    return jsonify(commen_success_res("",items))

# 删除评论
@user.route("/del/comment",methods=["DELETE","POST"])
def del_comment():

    form = del_comment_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    comment = CurriculumComments(id=form.id.data,aid=aid)
    if not comment.del_comment():
        return jsonify(del_err("删除评论失败"))

    return jsonify(commen_success_res("删除评论成功",""))
