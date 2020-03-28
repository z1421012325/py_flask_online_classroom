# coding=utf-8

import datetime
from sqlalchemy import and_
from OnlineClassroom.app.ext.plugins import db

from .catalog import Catalog
from .curriculum_comments import CurriculumComments
from .use_collections import Use_collections

from OnlineClassroom.app.utils.sql_result import sql_result_to_dict
from OnlineClassroom.app.utils.aliyun_oss import get_img_oss_url

"""
课程表
    CREATE TABLE `curriculums` (
    `cid` int NOT NULL AUTO_INCREMENT COMMENT '课程id',
    `cname` varchar(60) NOT NULL COMMENT '课程名字',
    `aid` int DEFAULT NULL COMMENT '外键 课程老师id',
    `price` float(10,2) DEFAULT '0.00' COMMENT '价格',
    `info` text COMMENT '课程介绍',
    `cimage` varchar(250) DEFAULT NULL COMMENT '阿里云oos直传',
    `create_at` datetime DEFAULT now() COMMENT '创建时间',
    `delete_at` datetime DEFAULT NULL COMMENT '删除时间',
    
    `admin_id` int comment '操作员工id',
    `open_at` datetime comment '操作时间'
    CONSTRAINT `admin_id` FOREIGN KEY (`admin_id`) REFERENCES `admins_user` (`aid`),
    
    PRIMARY KEY (`cid`),
    KEY `u_id` (`uid`),
    CONSTRAINT `curriculums_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `accounts` (`aid`)
    ) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;
"""

class Curriculums(db.Model):
    __tablename__ = "curriculums"
    cid = db.Column(db.Integer, primary_key=True, comment="课程id")
    cname = db.Column(db.String(60), nullable=False, comment="课程名字")
    aid = db.Column(db.Integer, db.ForeignKey("accounts.aid"), comment="外键 课程老师id")
    price = db.Column(db.Float(10, 2), default=0.0, comment=" 价格")
    info = db.Column(db.Text, comment=" 课程介绍")
    cimage = db.Column(db.String(250), comment="课程封面 阿里云oos直传")
    create_at = db.Column(db.DateTime,default=datetime.datetime.now(), comment="创建时间")
    delete_at = db.Column(db.DateTime, comment="删除时间")

    admin_id = db.Column(db.Integer, db.ForeignKey("admins_user.aid"), comment="操作员工id")
    open_at = db.Column(db.DateTime, comment="操作时间")

    catalogs = db.relationship(Catalog,backref="curriculum")
    comments = db.relationship(CurriculumComments,backref="curriculum")
    # purchase_records = db.relationship(ShoppingCarts,backref="curriculum")
    _use_collections = db.relationship(Use_collections,backref="_curriculum_")


    def __repr__(self):
        return "数据库{} {}-{}-{}-{}".format(self.__tablename__,self.aid,self.cid,self.cname,self.cimage)

    def __init__(self,cid=None,cname=None,aid=None,price=None,info=None,cimage=None,admin_aid=None):
        self.cname = cname
        self.aid = aid
        self.price = price
        self.info = info
        self.cimage = cimage
        self.cid = cid
        self.admin_aid = admin_aid


    def completion_oss_img_url(self):
        _img = get_img_oss_url(self.cimage,86400/2)
        return _img

    def save(self):
        self.create_at = datetime.datetime.now()
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

    # 查询多个课程并返回dict
    def query_curriculums_is_not_del(self,page=None,number=None):
        if page ==None:
            page = 1
        if number == None:
            number = 10

        items = {}
        list_item = []
        cs = self.query.filter_by(delete_at=None).paginate(int(page),int(number),False)
        for c in cs.items:
            item =  {
            "aid":c.aid,
            "cid": c.cid,
            "cname": c.cname,
            "price": str(c.price),
            "info": c.info,
            "cimage": c.completion_oss_img_url(),
            "create_at": c.json_time_is_null(),
            "delete_at":c.json_time_is_null()
                }
            list_item.append(item)

        items["datas"] = list_item
        items["len"] = len(cs.items)
        items["pages"] = cs.pages
        items["total"] = cs.total

        return items

    # 查询单个课程并返回dict
    def query_also_serialize(self):
        cc = self.query_curriculum_is_not_del()
        return cc.serialize_item()

    def query_curriculum_is_not_del(self):
        cc = self.query.filter_by(cid=self.cid, delete_at=None).first()
        if cc == None:
            return False
        return cc

    def serialize_item(self):
        item = {
            "aid":self.aid,
            "nickname":self.json_relation_user_nickname_is_null(),
            "cid": self.cid,
            "cname": self.cname,
            "price": str(self.price),
            "info": self.info,
            "cimage": self.completion_oss_img_url(),
            "create_at": self.json_time_is_null(),
            "delete_at":self.json_time_is_null()
        }
        return item

    def json_relation_user_nickname_is_null(self):
        if self.user == None:
            return ""
        return self.user.nickname

    def json_time_is_null(self):
        if self.create_at == None:
            return ""
        return self.create_at.strftime('%Y-%m-%d %H:%M:%S')

    def query_modify_curriculum_people(self):
        c = self.query.filter_by(cid=self.cid,delete_at=None).first()
        return c

    def modify_curriculum_info(self,name,price,info,cimage):
        if len(name)!= 0:
            self.cname = name
        if len(price) != 0:
            self.price = price
        if len(info) != 0:
            self.info = info
        if len(cimage) != 0:
            self.cimage = cimage
        return self.up_commit()


    def recommend_curriculums(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        currents = self.query.filter_by(aid=self.aid).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for c in currents.items:
            list_item.append(c.serialize_item())

        items["datas"] = list_item
        items["len"] = len(currents.items)
        items["pages"] = currents.pages
        items["total"] = currents.total

        return items


    def is_identity(self,aid=None):
        cc = self.query.filter_by(cid=self.cid).first()
        if cc == None:
            return False
        return int(cc.aid) == int(aid)


    def del_curriculums(self):
        c = self.query.filter_by(cid=self.cid).first()
        c.delete_at = datetime.datetime.now()
        return c.up_commit()


    def query_del_videos(self,page=1,number=20):
        if page == None:
            page = 1
        if number == None:
            number = 10

        ccs = self.query.filter(Curriculums.aid==self.aid,Curriculums.delete_at!=None).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for cc in ccs.items:
            list_item.append(cc.serialize_item())

        items['datas'] = list_item
        items['len'] = len(ccs.items)
        items["pages"] = ccs.pages
        items["total"] = ccs.total

        return items


    def recovery_curriculum(self):
        cc = self.query.filter_by(cid=self.cid,aid=self.aid).first()
        if cc == None:
            return False
        cc.delete_at = None
        return cc.up_commit()


    def get_purchase_records(self,page=1,number=10):
        if page== None:
            page = 1
        if number == None:
            number = 10

        c = self.query.filter_by(aid=self.aid).first()

        sql = "select u.aid as uid,u.nickname as nk,u.status as st,c.aid as c_aid,c.cname as name,c.price as price,c.cimage as img,c.create_at as at " \
              "from " \
              "shopping_carts as shop " \
              "join " \
              "accounts as u " \
              "on " \
              "u.aid = shop.aid " \
              "join curriculums as c " \
              "on " \
              "shop.cid = c.cid " \
              "where shop.cid in (select cid from curriculums where aid = {}) limit {},{}}".format(c.aid,page-1,page*number)
        results = db.session.execute(sql).fetchall()

        items = sql_result_to_dict(results)

        return items


    # order 默认查询排序  hot为(购买)热门排序,new 为最新排序
    def query_like_field_all(self,key,page=1,number=20,order=None):
        if key == None:
            key = ""
        if page == None or page<=0:
            page = 1
        if number == None or number<=0:
            number = 10

        items = {}
        list_item = []

        if order == "hot":
            results = self.sql_order_hot_results(key=key, page=page, number=number)
            for result in results:
                list_item.append(result)

            count = int(self.sql_search_hot_key_data_total(key=key))
            items["pages"] = int(count / number)
            items["len"] = results.__len__()
            items["total"] = count



        elif order == "new":
            results = self.sql_order_new_results(key=key, page=page, number=number)
            for result in results:
                list_item.append(result)

            count = int(self.sql_search_new_key_data_total(key=key))
            items["pages"] = int(count / number)
            items["len"] = results.__len__()
            items["total"] = count

        else:
            results = self.order_default_results(key=key, page=page, number=number)
            for result in results.items:
                list_item.append(result.serialize_item())

            items["len"] = len(results.items)
            items["pages"] = results.pages
            items["total"] = results.total


        items["datas"] = list_item

        return items

    def order_default_results(self,key,page,number):
        results = self.query.filter(Curriculums.cname.like("%" + key + "%")).paginate(int(page), int(number), False)
        return results

    def sql_order_hot_results(self, key, page, number):
        sql = """
            SELECT 
                count(*) AS count ,sp.cid AS s_cid ,c.* 
            FROM
                shopping_carts AS sp 
            join 
                curriculums AS c 
            ON 
                sp.cid = c.cid 
            WHERE 
                c.delete_at IS NULL AND c.cname like '%{}%'
            GROUP BY s_cid 
            ORDER BY s_cid DESC 
            limit {},{}
        """.format(key,(page-1)*number,number)
        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results,"cimage")

        return items

    def sql_order_new_results(self, key, page, number):
        sql = """
        SELECT 
            * 
        FROM 
            curriculums as c
        WHERE 
            delete_at IS NULL AND cname LIKE '%{}%' 
        ORDER BY create_at 
        DESC limit {},{}
        """.format(key,(page-1)*number,number)

        results = db.session.execute(sql).fetchall()

        items = sql_result_to_dict(results,"cimage")
        return items


    def sql_search_new_key_data_total(self, key):
        sql = """
        SELECT count(*) AS total FROM curriculums AS c WHERE c.delete_at IS NULL AND c.cname LIKE '%{}%'
        """.format(key)

        results = db.session.execute(sql).fetchall()
        _total = sql_result_to_dict(results)
        return _total[0].get("total")

    def sql_search_hot_key_data_total(self, key):
        sql = """
        SELECT 
                count(distinct c.cid) AS total 
            FROM 
                shopping_carts AS sp 
            JOIN 
                curriculums AS c 
            ON 
                sp.cid = c.cid 
            WHERE 
                c.delete_at is null and c.cname LIKE '%{}%'
        """.format(key)

        results = db.session.execute(sql).fetchall()
        _total = sql_result_to_dict(results)
        return _total[0].get("total")

    def get_arbitrarily_curriculum_count(self,day):
        # 处理一下,当前时间减去传递进来参数的天数时间,得到大于day_time的数据个数

        if day == None:
            day = 10
        query_time = datetime.datetime.now() - datetime.timedelta(days=int(day))

        count = self.query.filter(Curriculums.create_at>=query_time).count()

        return {"count":count}

    def get_arbitrarily_curriculum_is_del_count(self,day):

        if day == None:
            day = 10
        query_time = datetime.datetime.now() - datetime.timedelta(days=int(day))

        count = self.query.filter(Curriculums.create_at>=query_time,Curriculums.delete_at!=None).count()

        return {"count":count}


    def get_day_up_curriculums_count(self,day=10):
        sql = "select " \
              "DATE_FORMAT(c.create_at,'%Y-%m-%d') as dateDay,count(*) as countDay " \
              "from " \
              "curriculums as c " \
              "group by dateDay order by dateDay desc limit 0,{}".format(day)

        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items

    def get_curriculums(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10
        cs = self.query.filter().paginate(int(page),int(number),False)
        items = {}
        list_item = []

        for c in cs.items:
            list_item.append(c.serialize_item())

        items['datas'] = list_item
        items['len'] = len(cs.items)
        items["pages"] = cs.pages
        items["total"] = cs.total

        return items


    def get_del_curriculums(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        cs = self.query.filter(Curriculums.delete_at!=None).paginate(int(page),int(number),False)
        items = {}
        list_item = []

        for c in cs.items:
            item = {
                "aid": c.aid,
                "nickname": c.json_relation_user_nickname_is_null(),
                "cid": c.cid,
                "cname": c.cname,
                "price": str(c.price),
                "info": c.info,
                "cimage": c.completion_oss_img_url(),
                "create_at": c.json_time_is_null(),
                "delete_at": c.json_time_is_null(),
                "admin_aid": c.admin_id,
                "open_at": c.json_time_is_null()
            }
            list_item.append(item)
        items['datas'] = list_item
        items['len'] = len(cs.items)
        items["pages"] = cs.pages
        items["total"] = cs.total

        return items

    def admin_del_video(self,admin_aid):
        c = self.query.filter_by(cid=self.cid).first()
        if c == None:
            return False
        c.delete_at = datetime.datetime.now()
        c.admin_id = admin_aid
        c.open_at = datetime.datetime.now()
        return c.up_commit()

    def admin_adopt_video(self,admin_aid):
        c = self.query.filter_by(cid=self.cid).first()
        print("\n\n\n",c)
        if c == None:
            return False
        c.delete_at = None
        c.admin_id = admin_aid
        c.open_at = datetime.datetime.now()
        return c.up_commit()

    def get_curriculums_count(self):
        count = self.query.filter(Curriculums.delete_at==None).count()
        return {"count":count}