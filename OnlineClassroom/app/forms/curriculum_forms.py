# coding=utf-8

from .RequestBaseForm import RequestBaseForm
from wtforms import StringField,IntegerField,FloatField
from wtforms.validators import DataRequired




# 添加收藏表单
class add_collection_form(RequestBaseForm):
    cid = IntegerField("cid",validators=[DataRequired()])

# 取消收藏课程表单
class del_collection_form(RequestBaseForm):
    cid = IntegerField("cid",validators=[DataRequired()])


# 文件上传 (获取oss sign_url 用来上传和下载)
class get_oss_sign_url_form(RequestBaseForm):
    filename = StringField("filename",validators=[])
    filenames = StringField("filenames",validators=[])  # 多文件上传,文件名已逗号分割
    # 图片 img ,视频 video
    type = StringField("type",validators=[DataRequired()])


# 新增视频 保存上传视频(老师)  oss已经给与了put和geturl,上传参数中的url字段即可
class save_video_url_form(RequestBaseForm):
    name = StringField("name",validators=[DataRequired()])
    price = FloatField("price",validators=[DataRequired()])
    info = StringField("info", validators=[])
    cimage = StringField("cimage", validators=[])


# 修改视频信息(老师)
class modify_video_info_form(RequestBaseForm):
    cid = IntegerField("cid",validators=[DataRequired()])
    name = StringField("name", validators=[])
    price = FloatField("price", validators=[])
    info = StringField("info", validators=[])
    cimage = StringField("cimage", validators=[])


# 在已有视频的基础上添加视频
class add_follow_form(RequestBaseForm):
    cid = IntegerField("cid", validators=[DataRequired()])
    name = StringField("name", validators=[])
    url = FloatField("url", validators=[])


#  删除目录视频(老师)
class del_video_catalog_form(RequestBaseForm):
    id = IntegerField("id", validators=[DataRequired()])
    cid = IntegerField("cid", validators=[DataRequired()])



#  删除视频(老师)
class del_curriculum_form(RequestBaseForm):
    cid = IntegerField("cid", validators=[DataRequired()])


# 恢复下架视频(老师)
class recovery_curriculum_form(RequestBaseForm):
    cid = IntegerField("cid", validators=[DataRequired()])



# 购买
class shop_form(RequestBaseForm):
    cid = IntegerField("cid", validators=[DataRequired()])

