# coding=utf-8
import datetime
from OnlineClassroom.app.ext.plugins import db

"""

PASS

订单
CREATE TABLE `purchases` (
  `cid` int DEFAULT NULL COMMENT '外键 课程id',
  `aid` int DEFAULT NULL COMMENT '外键 用户id',
  `status` tinyint(1) DEFAULT NULL COMMENT '订单状态,默认为0未支付 支付为1',
  `price` float(10,2) DEFAULT NULL COMMENT '订单当时价格,数量不考虑因为是类似网易云课堂这种 只能买一份',
  `number` varchar(40) DEFAULT NULL COMMENT 'uuid流水号',
  `create_at` datetime DEFAULT now() COMMENT '创建时间',
  KEY `cid` (`cid`),
  KEY `aid` (`aid`),
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`),
  CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

class Purchases(db.Model):
    __tablename__ = "purchases"
    cid = db.Column(db.Integer,db.ForeignKey("curriculums.cid"),primary_key=True,comment="外键 课程id")
    aid = db.Column(db.Integer,db.ForeignKey("accounts.aid"),primary_key=True,comment="外键 用户id")

    status = db.Column(db.Integer,comment="订单状态,默认为0未支付 支付为1")
    price = db.Column(db.Float(10,2),comment="订单当时价格,数量不考虑因为是类似网易云课堂这种 只能买一份")
    number = db.Column(db.String(40),comment="uuid流水号")
    create_at = db.Column(db.DateTime,default=datetime.datetime.utcnow(),comment="创建时间")

    def __repr__(self):
        return "数据库{}".format(self.__tablename__)
