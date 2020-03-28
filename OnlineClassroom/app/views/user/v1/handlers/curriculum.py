#coding=utf-8

import os

from flask import Blueprint,jsonify,url_for,request

from OnlineClassroom.app.forms.curriculum_forms import *

from OnlineClassroom.app.models.use_collections import Use_collections
from OnlineClassroom.app.models.shopping_carts import *
from OnlineClassroom.app.models.money import *
from OnlineClassroom.app.models.account import *

from OnlineClassroom.app.serializetion.res_dict import *
from OnlineClassroom.app.utils.get_token import *
from OnlineClassroom.app.utils.aliyun_oss import *
from OnlineClassroom.app.utils.get_uuid import *


curriculum_ = Blueprint("curriculum_api_v1", __name__)


# 添加视频收藏
@curriculum_.route("/add/collection", methods=["POST"])
def add_collection():

    form = add_collection_form()
    if not form.validate_for_api():
        return jsonify(form.bindErr)

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    uc = Use_collections(aid=int(aid), cid=form.cid.data)
    if not uc.add_use_collection():
        return jsonify(add_err("课程收藏异常"))

    return jsonify(commen_success_res("课程收藏成功",""))


# 查看收藏视频
@curriculum_.route("/show/collection", methods=["GET"])
def show_collection():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    uc = Use_collections(aid=aid)
    items = uc.get_user_collections(page=request.args.get("page",1),number=request.args.get("number",10))

    return jsonify(commen_success_res("",items))


# 取消(删除)收藏
@curriculum_.route("/del/collection", methods=["DELETE", "POST"])
def del_collection():

    form = del_collection_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    uc = Use_collections(aid=aid, cid=form.cid.data)
    if not uc.del_collection():
        return jsonify(del_err(""))

    return jsonify(commen_success_res("删除成功",""))


# 课程页面
@curriculum_.route("/course/<int:cid>", methods=["GET"])
def course_curriculum(cid):

    cc = Curriculums(cid=cid)
    item = cc.query_also_serialize()

    return jsonify(commen_success_res("",item))

# 课程目录
@curriculum_.route("/course/detail/<int:cid>", methods=["GET"])
def course_detail_curriculum(cid):

    c = Catalog(cat_id=cid)
    items = c.query_catalogs()

    return jsonify(commen_success_res("",items))


# 课程评论
@curriculum_.route("/comment/<int:cid>", methods=["GET"])
def course_comment(cid):

    comment = CurriculumComments(cid=cid)
    items = comment.get_cid_comment_all(page=request.args.get("page", 1), number=request.args.get("number", 10))

    return jsonify(commen_success_res("",items))



# 开始学习,要对是否登录用户检测,或者课程价格为0or不为0检测(是否购买检测)
@curriculum_.route("/check/<int:cid>", methods=["GET"])
def curriculum_check(cid):

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    shop = ShoppingCarts(aid=int(aid),cid=cid)
    if not shop.is_record():
        return jsonify(commen_success_res("无购买记录并或者价格不为0",""))

    items = shop.get_curriculum__catalog()

    return jsonify(commen_success_res("",items))



# 该课程老师其他课程
@curriculum_.route("/recommend/<int:aid>", methods=["GET"])
def curriculum_recommend(aid):

    cc = Curriculums(aid=aid)
    items = cc.recommend_curriculums(page=request.args.get("page",1),number=request.args.get("number",10))

    return jsonify(commen_success_res("",items))





# todo 上传文件无法预览,下载也是无法观看  难道是origin限制?还是其他?
# 给予aliyun-oss凭证 让前端去aliyun-oss上传
@curriculum_.route("/get/oss/token", methods=["POST"])
def get_oss_token():

    form = get_oss_sign_url_form()
    if not form.validate_for_api():
        return form.bindErr

    if len(form.filename.data) == 0 or len(form.filenames.data) == 0:
        form.NoneErrToRes("参数都为空")
        return form.bindErr
    if form.type.data not in "img" or form.type.data not in "video":
        form.NoneErrToRes("文件类型不正确")
        return form.bindErr

    if len(form.filename.data) != 0:
        suffix = os.path.splitext(form.filename.data)
        if len(suffix[-1]) == 0 :
            form.NoneErrToRes("filename 无文件后缀")
            return form.bindErr
        # video or img
        oss_filename = "/".join((form.type.data,".".join((get_uuid(),suffix[-1]))))

        item = get_oss_bucket(oss_filename)
        item["filename"] = form.filename.data       # 上传文件名
        item["oss_filename"] = oss_filename         # oss存储文件名
        return jsonify(commen_success_res("",item))
    else:
        items = {}
        num = 0

        tps = ",".split(form.filenames.data)
        for i in tps:
            suffix = os.path.splitext(i)
            oss_filename = "/".join((form.type.data, ".".join((get_uuid(), suffix[-1]))))
            item = get_oss_bucket(oss_filename)
            item["filename"] = tps[num]
            item["oss_filename"] = oss_filename  # oss存储文件名

            num += 1
            item["number"] = num

            items[num] = item

        items["number"] = len(tps)
        return jsonify(commen_success_res("", items))



# 创建课程 保存上传信息(老师)
# 其中cimage为课程封面url,通过上面路由获取put和get地址,由前端上传至阿里云oss ,这里只接受返回的oss容器位置参数
@curriculum_.route("/save/new", methods=["POST"])
def save_new_video():

    form = save_video_url_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    u = Account(aid=aid)
    if not u.get_aid_is_UsersTeacherStatus():
        return jsonify(identity_err(""))

    cu = Curriculums(cname=form.name.data,price=form.price.data,
                     info=form.info.data,cimage=form.cimage.data,
                     aid=aid
                     )
    if not cu.save():
        return jsonify(add_err(""))

    return jsonify(commen_success_res("添加课程成功",""))




# 查看视频信息(老师)
@curriculum_.route("/see/<int:cid>", methods=["GET"])
def curriculum_see(cid):

    cc = Curriculums(cid=cid)
    item = cc.query_also_serialize()

    return jsonify(commen_success_res("",item))



# 修改视频信息(老师)
@curriculum_.route("/modify/video", methods=["POST"])
def modify_video_catalog():

    form = modify_video_info_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    cc = Curriculums(cid=form.cid.data)
    c = cc.query_modify_curriculum_people()
    if str(aid) != str(c.aid):
        return jsonify(identity_err(""))

    ok = c.modify_curriculum_info(name=form.name.data,price=form.price.data,info=form.info.data,cimage=form.cimage.data)
    if not ok:
        return jsonify(modify_err(""))

    item = c.serialize_item()
    return jsonify(commen_success_res("修改成功",item))


# 在已有课程的基础上添加视频
@curriculum_.route("/add/video/catalog", methods=["POST"])
def add_video_catalog():

    form = add_follow_form()
    if not form.validate_for_api():
        return form.bindErr

    c = Catalog(cat_id=form.cid.data,name=form.name.data,url=form.url.data)
    if not c.is_commit():
        return jsonify(add_err(""))

    return jsonify(commen_success_res("添加课程成功!",""))


#  删除目录视频(老师)
@curriculum_.route("/del/video/catalog", methods=["POST", "DELETE"])
def del_video_catalog():

    form = del_video_catalog_form()
    if not form.validate_for_api():
       return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    cc = Curriculums(cid=form.cid.data)
    c = cc.query_modify_curriculum_people()

    if int(aid) != int(c.aid):
        return jsonify(identity_err(""))

    cc = Catalog(id=form.id.data,cat_id=form.cid.data)
    obj = cc.query_catalog_object()
    if not obj.del_catalog():
        return jsonify(del_err(""))

    return jsonify(commen_success_res("删除目录视频成功",""))






# 下架视频
@curriculum_.route("/del/video", methods=["POST","DELETE"])
def del_video():

    form = del_curriculum_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    cc = Curriculums(cid=form.cid.data)
    if not cc.is_identity(aid):
        return jsonify(identity_err(""))

    if not cc.del_curriculums():
        return jsonify(del_err(""))

    return jsonify(commen_success_res("下架课程成功", ""))



# 查看下架的视频
@curriculum_.route("/show/video", methods=["GET"])
def show_video():

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    cc = Curriculums(aid=aid)
    items = cc.query_del_videos(page=request.args.get("page",1),number=request.args.get("number",10))

    return jsonify(commen_success_res("",items))


# 恢复下架视频(老师)
@curriculum_.route("/recovery/video", methods=["POST"])
def recovery_video():

    form = recovery_curriculum_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    cc = Curriculums(aid=aid,cid=form.cid.data)
    if not cc.recovery_curriculum():
        return jsonify(modify_err(""))

    return jsonify(commen_success_res("上架视频成功",""))


# 购买
@curriculum_.route("/add/shopping", methods=["POST"])
def add_shopping():

    form = shop_form()
    if not form.validate_for_api():
        return form.bindErr

    token = requst_get_token()
    ok, aid = check_token(token)
    if not ok:
        return jsonify(token_err(""))

    c = Curriculums(cid=form.cid.data)      # cid 为 1
    cc = c.query_curriculum_is_not_del()
    if not cc :
        return jsonify(query_err("该课程不存在"))

    shop = ShoppingCarts(aid=aid,cid=form.cid.data)
    if shop.is_purchase():
        return jsonify(commen_success_res("已经购买该课程",""))

    """
        订单,支付宝,微信交易逻辑
            服务端返回支付url(含回拨url 单号等数据),前端跳转支付url网关
            例  {
                    "zfb_url":"http://zfb.io/xxxx/callback_url=xxxx/number=xxxxx",
                    "callback_url":"xxxx",              // 回拨url 接受支付结果
                    "number":"xxxx",                    // 唯一单号,作为支付凭证,平台返回该单号
                }
            因支付url附带callback url,另开一个接口接受支付平台返回支付结果和对应单号并保存数据库中
            前端将单号作为参数对服务端接口进行间隔的请求,根据结果显示相应的数据
            所以还需要两个接口,一个接受支付平台结果,查询支付结果
        省略为默认购买,假设直接将用户购买金额数据转入对应用户金额账号中
    """

    money = Money(aid=cc.aid,money=cc.price)
    if not money.add_user_money(add_money=cc.price):
        return jsonify(shop_err(""))

    if not shop.save():
        return jsonify(shop_err(""))

    item = cc.serialize_item()

    return jsonify(commen_success_res("购买课程成功",item))
