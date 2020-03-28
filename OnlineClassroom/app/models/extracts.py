# coding=utf-8
import datetime
from OnlineClassroom.app.ext.plugins import db
from OnlineClassroom.app.utils.get_uuid import *

from .money import Money

from OnlineClassroom.app.utils.sql_result import sql_result_to_dict

"""
金额提取
CREATE TABLE `extracts` (
  `eid` int NOT NULL AUTO_INCREMENT COMMENT '主键自增长',
  `create_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `t_money` float(10,2) DEFAULT NULL COMMENT '提取金额',
  `divide` float(10,2) DEFAULT 0.05 COMMENT '站点分成,默认为5%',
  `actual_money` float(10,2) DEFAULT NULL COMMENT '实际提成',
  `aid` int DEFAULT NULL COMMENT '外键 用户id',
  `number` varchar(35) DEFAULT NULL COMMENT '流水号',
  `status` int DEFAULT 0 COMMENT '转账交易状态 0 为显示转账但是未到达,1为转账成功,2为转账失败',
  PRIMARY KEY (`eid`),
  KEY `aid` (`aid`),
  CONSTRAINT `extracts_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=100000 DEFAULT CHARSET=utf8
"""
class Extracts(db.Model):
    __tablename__ = "extracts"
    eid = db.Column(db.Integer, primary_key=True, comment="外键 课程id")
    create_at = db.Column(db.DateTime,default=datetime.datetime.utcnow(), comment="创建时间")
    t_money = db.Column(db.Float(10,2), comment="提取金额")
    divide = db.Column(db.Float(10, 2),default=0.05, comment="站点分成,默认为5%")
    actual_money = db.Column(db.Float(10, 2), comment="实际提成")
    aid = db.Column(db.Integer, db.ForeignKey("accounts.aid"),comment="外键 用户id")
    number = db.Column(db.String(35),  comment="流水号")
    status = db.Column(db.Integer, comment="转账交易状态 0 为显示转账但是未到达,1为转账成功,2为转账失败")

    status_not_complete = 0
    status_complete = 1
    status_fail = 2

    money_divide = 0.05

    def __repr__(self):
        return "数据库{}".format(self.__tablename__)

    def __init__(self,aid=None,t_money=None,actual_money=None,number=None):
        self.aid = aid
        self.t_money = t_money
        self.divide = self.money_divide
        self.actual_money = actual_money
        self.number = number
        self.status = self.status_not_complete
        self.create_at = datetime.datetime.utcnow()

    def new_extract(self,aid=None,t_money=None,actual_money=None):
        self.aid = aid
        self.t_money = t_money
        self.actual_money = actual_money
        self.number = get_uuid()

    def save(self,m):

        _m = Money.query.filter_by(aid=self.aid).first()
        _m.money = float(_m.money) - float(m)
        _m.up_commit()

        return self.is_commit()

    def up_commit(self):
        try:
            db.session.commit()
            return True
        except Extracts as e:
            db.session.rollback()
            return False

    def is_commit(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Extracts as e:
            db.session.rollback()
            return False

    def get_number(self):
        return self.number

    def serializetion_item(self):
        item = {
            "aid": self.aid,
            "eid": self.eid,
            "t_money": str(self.t_money),
            "divide": str(self.divide),
            "actual_money": str(self.actual_money),
            "number": str(self.number),
            "status":self.status,
            "create_at":self.json_create_at_is_null()
        }
        return item

    def json_create_at_is_null(self):
        if self.create_at == None:
            return ""
        return self.create_at.strftime('%Y-%m-%d %H:%M:%S')

    def query_user_extracts(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        exs = self.query.filter_by(aid=self.aid).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for ex in exs.items:
            list_item.append(ex.serializetion_item())

        items["datas"] = list_item
        items["len"] = len(exs.items)
        items["pages"] = exs.pages
        items["total"] = exs.total

        return items



    def get_day_sum_money(self,day):
        sql = """
            select date_format(create_at,'%Y-%m-%d')as dateDay,sum(t_money) as moneyDay from extracts group by dateDay order by dateDay limit 0,{}
        """.format(day)

        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items


    def get_teacher_royalty_money(self,day):
        sql = """ 
        select date_format(create_at,'%Y-%m-%d') as dateDay ,sum(actual_money) as money_total from extracts group by dateDay order by dateDay desc limit 0,{}
        """.format(day)

        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items