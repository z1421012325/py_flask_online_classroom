# coding=utf-8

from OnlineClassroom.app.ext.plugins import db
from .extracts import *

"""
用户金额
CREATE TABLE `money` (
  `aid` int DEFAULT NULL COMMENT '外键用户表id,唯一',
  `money` float(10,2) DEFAULT '0.00' COMMENT '金钱',
  `version` int DEFAULT NULL COMMENT '乐观锁,版本控制',
  UNIQUE KEY `aid` (`aid`),
  CONSTRAINT `money_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class Money(db.Model):
    __tablename__ = "money"

    aid = db.Column(db.Integer,db.ForeignKey("accounts.aid"), primary_key=True,comment="外键用户表id,唯一")
    money = db.Column(db.Float(10,2), default=0.00, comment="金钱")
    version = db.Column(db.Integer, comment="乐观锁,版本控制")

    def __repr__(self):
        return "数据库{} {}_{}_{}".format(self.__tablename__,self.aid,self.money,self.version)

    def __init__(self,aid=None,money=None):
        self.aid = aid
        self.money = money

    def add_user_money(self,add_money):
        m = self.query.filter_by(aid=self.aid).first()
        if m == None:
            ok = self.is_query_is_null_new_account()
            if not ok:
                return False

        up_money = float(m.money) + float(add_money)
        m.money = up_money
        m.version += 1
        return m.up_commit()

    def is_query_is_null_new_account(self):
        self.aid = self.aid
        self.money = 0.00
        self.version = 1
        return self.is_commit()

    # commit
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

    # test_ commit
    def test_with_is_commit(self):
        with db.session.commit():
            pass


    def get_user_money(self):
        m = self.query.filter_by(aid=self.aid).first()
        return m.money


