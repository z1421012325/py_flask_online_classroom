# coding=utf-8

import datetime
from OnlineClassroom.app.ext.plugins import db

from .account import *

"""
课程评价
CREATE TABLE `curriculum_comments` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `cid` int DEFAULT NULL COMMENT '外键 课程id',
  `aid` int DEFAULT NULL COMMENT '外键 用户id',
  `number` tinyint(10) DEFAULT NULL COMMENT '评价分数',
  `comment` varchar(300) DEFAULT NULL COMMENT '评价',
  `create_at` datetime DEFAULT now() COMMENT '创建时间',
  `delete_at` datetime DEFAULT NULL COMMENT '删除时间',
  
   `admin_id` int comment '操作员工id',
   `open_at` datetime comment '操作时间'
   CONSTRAINT `admin_id` FOREIGN KEY (`admin_id`) REFERENCES `admins_user` (`aid`),
  
  UNIQUE KEY `ac_id` (`aid`,`cid`),
  CONSTRAINT `curriculum_comments_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`),
  CONSTRAINT `curriculum_comments_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""
class CurriculumComments(db.Model):
    __tablename__ = "curriculum_comments"
    id = db.Column(db.Integer,primary_key=True,comment="主键")
    cid = db.Column(db.Integer, db.ForeignKey("curriculums.cid"),comment="外键 课程id") # primary_key=True
    aid = db.Column(db.Integer, db.ForeignKey("accounts.aid"),comment="外键 用户id") # primary_key=True
    number = db.Column(db.Integer,comment="评价分数")
    comment = db.Column(db.String(300), comment="评价")
    create_at = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    delete_at = db.Column(db.DateTime)

    admin_id = db.Column(db.Integer, db.ForeignKey("admins_user.aid"), comment="操作员工id")
    open_at = db.Column(db.DateTime, comment="操作时间")

    def __repr__(self):
        return "数据库{}".format(self.__tablename__)

    def __init__(self,cid=None,aid=None,number=None,comment=None,id=None):
        self.cid = cid
        self.aid = aid
        self.number = number
        self.comment = comment
        self.id=id


    def get_cid_comment_all(self, page=1, number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10
        comments = self.query.filter_by(cid=self.cid,delete_at=None).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for comment in comments.items:
            item = comment.serializetion_item()
            list_item.append(item)

        items["datas"] = list_item
        items["len"] = len(comments.items)
        items["pages"] = comments.pages
        items["total"] = comments.total

        return items

    def get_aid_comment_all(self, page=1, number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10
        comments = self.query.filter_by(aid=self.aid,delete_at=None).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for comment in comments.items:
            list_item.append(comment.serializetion_item())

        items["datas"] = list_item
        items["len"] = len(comments.items)
        items["pages"] = comments.pages
        items["total"] = comments.total

        return items


    def serializetion_item(self):
        item = {
            "id":self.id,
            "aid":self.aid,
            "cid":self.cid,
            "name":self.user.nickname,
            "c_name":self.curriculum.cname,
            "number": self.number,
            "comment": self.comment,
            "ct": self.serializetion_time_json_is_null(self.create_at),
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

    def up_commit(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def save(self):
        if self.number == None:
            self.number = 0
        self.create_at = datetime.datetime.utcnow()
        return self.is_commit()


    def query_user_comments(self,page=1,number=20):
        if page == None:
            page = 1
        if number == None:
            number = 10

        comments = self.query.filter_by(aid=self.aid,delete_at=None).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for comment in comments.items:
            list_item.append(comment.serializetion_item())

        items["datas"] = list_item
        items["len"] = len(comments.items)
        items["pages"] = comments.pages
        items["total"] = comments.total

        return items

    def del_comment(self):
        comment = self.query.filter_by(id=self.id,aid=self.aid).first()
        comment.delete_at = datetime.datetime.utcnow()
        return comment.up_commit()


    def get_commnets(self, page=1, number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        comments = self.query.filter().paginate(int(page),int(number),False)

        items = {}
        list_item = []
        for comment in comments.items:
            item = {
                "id": comment.id,
                "aid": comment.aid,
                "cid": comment.cid,
                "name": comment.user.nickname,
                "c_name": comment.curriculum.cname,
                "number": comment.number,
                "comment": comment.comment,
                "ct": comment.serializetion_time_json_is_null(comment.create_at),
                "dt": comment.serializetion_time_json_is_null(comment.delete_at)
            }
            list_item.append(item)

        items["datas"] = list_item
        items["len"] = len(comments.items)
        items["pages"] = comments.pages
        items["total"] = comments.total

        return items


    def admin_del_comment(self,admin_aid):
        comment = self.query.filter_by(id=self.id).first()
        if comment == None:
            return False

        comment.delete_at = datetime.datetime.now()
        comment.open_at = datetime.datetime.now()
        comment.admin_id = admin_aid
        return comment.up_commit()

    def admin_recovery_comment(self,admin_aid):
        comment = self.query.filter_by(id=self.id).first()
        comment.delete_at = None
        comment.open_at = datetime.datetime.now()
        comment.admin_id = admin_aid
        return comment.up_commit()