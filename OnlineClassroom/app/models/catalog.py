# coding=utf-8

import datetime
from OnlineClassroom.app.ext.plugins import db
from OnlineClassroom.app.utils.aliyun_oss import *

"""
课程目录
 CREATE TABLE `catalog` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '目录id',
  `cat_id` int DEFAULT NULL COMMENT '外键 课程id',
  `name` varchar(50) DEFAULT NULL COMMENT '课程目录名称',
  `url` varchar(255) DEFAULT NULL COMMENT '目录地址',
  `create_at` datetime DEFAULT now() COMMENT '一个课程多个目录,根据时间排序',
  `delete_at` datetime DEFAULT null COMMENT '删除时间,软删除',
  KEY `cat_id` (`cat_id`),
  CONSTRAINT `catalog_ibfk_1` FOREIGN KEY (`cat_id`) REFERENCES `curriculums` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""


class Catalog(db.Model):
    __tablename__ = "catalog"

    id = db.Column(db.Integer,primary_key=True, comment="目录id")
    cat_id = db.Column(db.Integer, db.ForeignKey("curriculums.cid"), comment="外键 课程id")
    name = db.Column(db.String(50),nullable=False,comment="课程目录名称")
    url = db.Column(db.String(255),nullable=False,comment="目录地址")
    create_at = db.Column(db.DateTime,default=datetime.datetime.utcnow(),comment="一个课程多个目录,根据时间排序")
    delete_at = db.Column(db.DateTime,comment="删除时间,软删除")

    def __repr__(self):
        return "数据库{}".format(self.__tablename__)


    def __init__(self,id=None,cat_id=None,name=None,url=None):
        self.id = id
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.create_at = datetime.datetime.now()


    def query_catalogs(self):
        catalogs = self.query.filter_by(cat_id=self.cat_id, delete_at=None).all()

        items = {}
        list_time = []

        for catalog in catalogs:
            list_time.append(catalog.serializetion_itme())

        items["datas"] = list_time
        items["len"] = len(catalogs)
        return items

    def query_catalog_object(self):
        return self.query.filter_by(cat_id=self.cat_id,id=self.id, delete_at=None).first()

    def del_catalog(self):
        self.delete_at = datetime.datetime.now()
        return self.up_commit()

    def up_commit(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def completion_oss_img_url(self):
        _url = get_img_oss_url(self.url,86400/2)
        return _url

    def serializetion_itme(self):
        item = {
            "id" : self.id,
            "cat_id" : self.cat_id,
            "name" : self.name,
            "url" : self.completion_oss_img_url(),
            "ct":self.serializetion_time_json_is_null(self.create_at),
            "dt":self.serializetion_time_json_is_null(self.delete_at)
        }
        return item

    def serializetion_time_json_is_null(self, time):
        if time == None:
            return ""
        if isinstance(time, datetime.datetime) or isinstance(time, datetime.time):
            return time.strftime('%Y-%m-%d %H:%M:%S')
        return ""


    def is_commit(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

