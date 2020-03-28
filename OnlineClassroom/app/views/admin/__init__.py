# coding=utf-8

from flask import Blueprint,jsonify

from OnlineClassroom.app.forms.admin_forms import *
from OnlineClassroom.app.forms.paginate_form import *
from OnlineClassroom.app.serializetion.res_dict import *

from OnlineClassroom.app.models.admin_user import *
from OnlineClassroom.app.models.admin_role import *
from OnlineClassroom.app.models.curriculums import *
from OnlineClassroom.app.models.account import *
from OnlineClassroom.app.models.curriculum_comments import *
from OnlineClassroom.app.models.shopping_carts import *
from OnlineClassroom.app.models.extracts import *


from OnlineClassroom.app.utils.get_token import *

admin = Blueprint('admin_api_v1',__name__)

# 注册, todo  zzzzzzzzz
@admin.route("/registry", methods=["POST"])
def registry():

    form = registry_form()
    if not form.validate_for_api():
        return form.bindErr

    u = Admin_Users(username=form.username.data,pswd=form.pswd.data,r_id=form.rid.data)
    if not u.save():
        return jsonify(add_err(""))

    return jsonify(registry_success_res())

# 登录 zzzzzzzzzzzz
@admin.route("/login", methods=["POST"])
def login():

    form = login_form()
    if not form.validate_for_api():
        return form.bindErr

    u = Admin_Users(username=form.username.data)
    _u,ok = u.check_login_user_pswd(form.pswd.data)
    if not ok:
        if _u == None or not ok:
            return jsonify(pswd_check_err("账号未激活"))
        return jsonify(pswd_check_err(""))
    token = create_admin_token(_u.get_aid(),_u.get_username(),_u.get_rid())
    dict_res = {
        "code":10000,
        "msg":"success",
        "data":token
    }

    return jsonify(dict_res)

# 退出  zzzzzzz
@admin.route("/logout", methods=["POST"])
def logout():
    token = requst_get_token()
    ok, data = check_admin_token(token)
    return jsonify(commen_success_res("logout out ",data))


# 拥有管理权限人员对普通员工账号激活,只能激活下一级,平级无法激活  zzzz
@admin.route("/activation/user", methods=["POST"])
def activation_user():

    form = activation_user_status_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    r_id = int(data.get("r_id"))

    u = Admin_Users(aid=form.aid.data)
    _u = u.get_user_aid_unactivation()

    if _u == None:
        return jsonify(modify_err("账号已激活"))
    if r_id < _u.r_id:
        return jsonify(modify_err("权限等级过低,无法激活"))

    if not _u.modift_auth_status():
        return jsonify(modify_err("账号状态异常"))

    return jsonify(commen_success_res("激活成功",""))


# 员工修改本身账号密码  zzzz
@admin.route("/modify/pswd", methods=["POST"])
def modify_is_pswd():

    form = modify_pswd_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Admin_Users(aid=data.get("aid"), username=data.get("username"))
    _u,ok = u.check_login_user_pswd(form.old.data)
    if not ok :
        return jsonify(modify_err("密码错误"))

    if not _u.modify_pswd(form.new.data):
        return jsonify(modify_err("修改密码错误"))

    return jsonify(commen_success_res("修改密码成功",""))

# 修改下级员工权限  zzzzz
@admin.route("/modify/grade", methods=["POST"])
def modify_is_grade():

    form = modify_user_status_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    r_id = int(data.get("r_id"))

    u = Admin_Users(aid=form.aid.data)
    _u = u.get_user_aid_activation()

    if _u == None:
        return jsonify(modify_err("没有改账号存在!"))
    if r_id <= _u.r_id:
        return jsonify(modify_err("权限等级过低,无法修改"))

    if not _u.modift_auth_status(form.grade.data):
        return jsonify(modify_err("账号状态修改异常或者权限异常"))

    return jsonify(commen_success_res("修改权限成功", ""))


# 查看未激活员工账号(小于查询账户权限的未激活账号)   zzzzzzzzzzz
@admin.route("/show/user/unstatus", methods=["GET"])
def show_user_unstatus():

    form = page_form()

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Admin_Users()
    items = u.get_unactivation_accounts(page=form.page.data,number=form.number.data,r_id=data.get("r_id"))

    return jsonify(commen_success_res("",items))


# 查看离职员工账号  zzzzzzzzz
@admin.route("/show/user/leave", methods=["GET"])
def show_user_leave():

    form = page_form()
    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Admin_Users()
    items = u.get_leave_accounts(page=form.page.data, number=form.number.data,r_id=data.get("r_id"))

    return jsonify(commen_success_res("", items))


# 查看所有员工激活账号  zzzz
@admin.route("/show/user/all", methods=["GET"])
def show_user_all():

    form = page_form()

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Admin_Users()
    items = u.get_all_accounts(page=form.page.data, number=form.number.data,r_id=data.get("r_id"))

    return jsonify(commen_success_res("", items))

# 查看所有员工未激活账号  zzzz
@admin.route("/show/unuser/all", methods=["GET"])
def show_unuser_all():

    form = page_form()
    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Admin_Users()
    items = u.get_all_unaccounts(page=form.page.data, number=form.number.data,r_id=data.get("r_id"))

    return jsonify(commen_success_res("", items))


# 查看视频和总个数  zzzzzzzz
@admin.route("/show/video/total", methods=["GET","POST"])
def show_video_total():
    c = Curriculums()
    item = c.get_curriculums_count()
    return jsonify(commen_success_res("", item))



# 查看一定天数之内的视频总数 zzzzzz
@admin.route("/show/curriculum/total/<int:day>", methods=["GET"])
def show_curriculum_total_day(day):

    c = Curriculums()
    items = c.get_arbitrarily_curriculum_count(day=day)
    return jsonify(commen_success_res("", items))


# 查看一定天数之内被删的视频总数  zzzz
@admin.route("/show/curriculum/del/total/<int:day>", methods=["GET"])
def show_curriculum_is_del_total_day(day):

    c = Curriculums()
    items = c.get_arbitrarily_curriculum_is_del_count(day=day)
    return jsonify(commen_success_res("", items))


# 根据天数查看当天视频上传个数 zzzz
@admin.route("/show/curriculum/count/<int:day>", methods=["GET"])
def show_curriculum_count_day(day):

    c = Curriculums()
    items = c.get_day_up_curriculums_count(day)
    return jsonify(commen_success_res("", items))




# 根据天数查看正常注册的人数 zzzzzzzz
@admin.route("/show/user/count/<int:day>", methods=["GET"])
def show_user_count_day(day):

    u = Account()
    items = u.get_day_registry_count(day)
    return jsonify(commen_success_res("", items))


# 查看总注册人数  zzzz
@admin.route("/show/user/total", methods=["GET"])
def show_user_total():
    u = Account()
    items = u.get_registry_counts()
    return jsonify(commen_success_res("", items))



# 查看用户列表  zzzzzz
@admin.route("/show/users", methods=["GET"])
def show_users_list():
    form = page_form()

    u = Account()
    items = u.get_users(page=form.page.data,number=form.number.data)

    return jsonify(commen_success_res("", items))

# 封禁用户  zzzzz
@admin.route("/del/prohibit/user", methods=["POST"])
def del_prohibit_user():

    form = del_prohibit_user_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Account(aid=form.aid.data)
    if not u.prohibit_user(int(data.get("aid"))):
        return jsonify(modify_err(""))

    return jsonify(commen_success_res("封禁用户成功",""))



# 查看封禁用户  zzzzzzz
@admin.route("/show/prohibit/users", methods=["GET"])
def show_prohibit_users():

    form = page_form()

    u = Account()
    items = u.get_prohibit_users(page=form.page.data,number=form.number.data)

    return jsonify(commen_success_res("",items))


# 解封用户  zzzzzzz
@admin.route("/adopt/user", methods=["POST"])
def adopt_user():

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    form = adopt_user_form()
    if not form.validate_for_api():
        return form.bindErr

    u = Account(aid=form.aid.data)
    if not u.reduction_prohibit_user(admin_aid=data.get("aid")):
        return jsonify(modify_err("解封用户异常"))

    return jsonify(commen_success_res("解封用户成功",""))

# 查看视频  zzzzzz
@admin.route("/show/list/video", methods=["GET"])
def show_list_video():

    form = page_form()
    c = Curriculums()
    items = c.get_curriculums(page=form.page.data,number=form.number.data)
    return jsonify(commen_success_res("",items))

# 查看下架视频  zzz
@admin.route("/show/del/videos", methods=["GET"])
def show_del_list_video():

    form = page_form()
    c = Curriculums()
    items = c.get_del_curriculums(page=form.page.data,number=form.number.data)
    return jsonify(commen_success_res("",items))


# 下架视频 zzzz
@admin.route("/del/video", methods=["POST"])
def del_video():

    form = admin_del_video_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    c = Curriculums(cid=form.cid.data)
    if not c.admin_del_video(admin_aid=int(data.get("aid"))):
        return jsonify(modify_err("删除失败"))

    return jsonify(commen_success_res("删除成功", ""))

# 恢复视频  zzzz
@admin.route("/adopt/video", methods=["POST"])
def adopt_video():

    form = admin_recovery_video_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    c = Curriculums(cid=form.cid.data)
    if not c.admin_adopt_video(admin_aid=int(data.get("aid"))):
        return jsonify(modify_err("恢复视频失败"))

    return jsonify(commen_success_res("恢复视频成功",""))


# 查看评论  zzzz
@admin.route("/show/comments", methods=["GET"])
def show_comments():

    form = page_form()

    comment = CurriculumComments()
    items = comment.get_commnets(page=form.page.data,number=form.number.data)
    return jsonify(commen_success_res("",items))


# 删除评论  zzzzzz
@admin.route("/del/comment", methods=["POST"])
def del_comment():

    form = admin_del_comment_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    comment = CurriculumComments(id=form.id.data)
    if not comment.admin_del_comment(admin_aid=int(data.get("aid"))):
        return jsonify(modify_err("删除评论失败"))

    return jsonify(commen_success_res("删除评论成功",""))


# 恢复评论 zzzzzz
@admin.route("/adopt/comment", methods=["POST"])
def adopt_comment():
    form = admin_del_comment_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, data = check_admin_token(token)
    if not ok:
        return jsonify(token_err(""))

    comment = CurriculumComments(id=form.id.data)
    if not comment.admin_recovery_comment(admin_aid=int(data.get("aid"))):
        return jsonify(modify_err("恢复评论失败"))

    return jsonify(commen_success_res("恢复评论成功",""))


# 根据天数查看当天下单金额  zzzzzz
@admin.route("/show/money/<int:day>", methods=["GET"])
def show_day_money_day(day):

    shop = ShoppingCarts()
    items = shop.get_days_shop_effective_sum(day)

    return jsonify(commen_success_res("",items))


# 总共下单金额  zzzzzz
@admin.route("/show/money/total", methods=["GET"])
def show_total_money():
    shop = ShoppingCarts()
    items = shop.get_monerys()
    return jsonify(commen_success_res("", items))


# 根据天数查看当天金额  zzzzzz
@admin.route("/show/royalty/money/<int:day>", methods=["GET"])
def show_site_royalty_money_day(day):

    ex = Extracts()
    items = ex.get_day_sum_money(day)
    return jsonify(commen_success_res("", items))


# 根据天数查看被老师提取出去的金额总数 zzzzzz
@admin.route("/show/teacher/money/<int:day>", methods=["GET"])
def show_teacher_royalty_money(day):
    ex = Extracts()
    items = ex.get_teacher_royalty_money(day)
    return jsonify(commen_success_res("", items))


