# coding=utf-8

import datetime
from OnlineClassroom.app.ext.plugins import db

"""
用户收藏课程
CREATE TABLE `use_collections` (
  `aid` int DEFAULT NULL COMMENT '外键 用户id',
  `cid` int DEFAULT NULL COMMENT '外键 课程id',
  `create_at` datetime DEFAULT now() COMMENT '创建时间',
  `delete_at` datetime DEFAULT null COMMENT '删除时间,软删除',
  KEY `cid` (`cid`),
  KEY `aid` (`aid`),
  CONSTRAINT `use_collections_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`),
  CONSTRAINT `use_collections_ibfk_2` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class Use_collections(db.Model):
    __tablename__ = "use_collections"
    aid = db.Column(db.Integer,db.ForeignKey("accounts.aid"),primary_key=True, comment="外键 用户id")
    cid = db.Column(db.Integer, db.ForeignKey("curriculums.cid"),primary_key=True, comment="外键 课程id")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now(), comment="一个课程多个目录,根据时间排序")
    delete_at = db.Column(db.DateTime, comment="删除时间,软删除")

    curriculums = db.relationship("Curriculums", backref="use_collections")



    def __repr__(self):
        return "数据库{}".format(self.__tablename__)

    def __init__(self,aid=None,cid=None):
        self.aid = aid
        self.cid = cid
        self.create_at = datetime.datetime.now()



    def add_use_collection(self):
        return self.is_commit()


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


    # 查询收藏课程
    # todo 测试一下
    def query_use_curriculms(self):

        datas = {}
        list_items = []

        for cc in self.curriculums:
            list_items.append(cc)

        datas["data"] = list_items

        # 查询个数和总个数
        total = 0
        datas["total"] = total
        current_number = 0
        datas["current_number"] = current_number

        return datas


    def del_collection(self):
        c = self.query.filter_by(aid=self.aid,cid=self.cid).first()
        c.delete_at = datetime.datetime.now()
        return c.up_commit()


    def get_user_collections(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        colls = self.query.filter_by(aid=self.aid,delete_at=None).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for c in colls.items:
            list_item.append(c._curriculum_.serialize_item())

        items["datas"] = list_item
        items["len"] = len(colls.items)
        items["pages"] = colls.pages
        items["total"] = colls.total

        return items

    def serializetion_json(self):
        item = {
            "aid":self.aid,
            "cid": self.cid,
            "name":self._user.nickname,
            "c_title":self._curriculum_.cname,
            "create_at": self.serializetion_time_json_is_null(self.create_at),
            "delete_at": self.serializetion_time_json_is_null(self.delete_at),
        }
        return item

    def serializetion_time_json_is_null(self,time):
        if time == None:
            return ""
        if isinstance(time,datetime.datetime) or isinstance(time,datetime.time):
            return time.strftime('%Y-%m-%d %H:%M:%S')
        return ""
