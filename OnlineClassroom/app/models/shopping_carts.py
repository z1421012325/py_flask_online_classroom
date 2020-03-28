# coding=utf-8


import datetime
from OnlineClassroom.app.ext.plugins import db
from .curriculums import *
from .account import *
from .catalog import *
"""
购买记录
CREATE TABLE `shopping_carts` (
  `aid` int DEFAULT NULL COMMENT '外键 用户id',
  `cid` int DEFAULT NULL COMMENT '外键 课程id',
  `number` int DEFAULT '1' COMMENT '课程数量,但是是网易云课堂类似的,默认就是1买把...',
  `price` float(10,2) DEFAULT '0.00' COMMENT '购买时价格',
  `create_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  KEY `uid` (`aid`),
  KEY `cid` (`cid`),
  CONSTRAINT `shopping_carts_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`),
  CONSTRAINT `shopping_carts_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class ShoppingCarts(db.Model):
    __tablename__ = "shopping_carts"

    aid = db.Column(db.Integer,db.ForeignKey("accounts.aid"),primary_key=True, comment="外键 用户id")
    cid = db.Column(db.Integer,db.ForeignKey("curriculums.cid"),primary_key=True,comment="外键 课程id")
    number = db.Column(db.Integer,default=1)
    price = db.Column(db.Float(10,2),default=0.00)
    create_at = db.Column(db.DateTime,default=datetime.datetime.utcnow(),comment="创建时间")

    _curriculum = db.relationship(Curriculums,backref="shop")
    # user = db.relationship(Account,backref="shops")


    def __repr__(self):
        return "数据库{} {}_{}_{}_{}".format(self.__tablename__,self.cid,self.aid,self.number,self.price)

    def __init__(self,aid=None,cid=None,price=None):
        self.aid =aid
        self.cid = cid
        self.number = 1
        self.price = price
        self.create_at = datetime.datetime.now()

    # 查询是否购买或者价格为0
    def is_record(self):
        shop = self.query.filter_by(aid=self.aid,cid=self.cid).first()
        if shop == None:
            cu = Curriculums.query.filter_by(cid=self.cid).first()
            if cu.price <= float(0):
                return True
        else:
            if shop.number != 1:
                if not shop.curriculum.price <= float(0):
                    return False
                return True
            elif shop.number == 1:
                return True


    def get_curriculum__catalog(self):

        _catalogs = Catalog.query.filter_by(cat_id=self.cid).all()

        items = {}
        list_time = []

        for catalog in _catalogs:
            list_time.append(catalog.serializetion_itme())

        items["datas"] = list_time
        items["len"] = len(_catalogs)
        return items

    def is_purchase(self):
        shop = self.query.filter(ShoppingCarts.aid==self.aid,ShoppingCarts.cid==self.cid).first()
        if shop == None:
            return False
        return shop.number == 1

    def save(self):
        self.number = 1
        self.create_at = datetime.datetime.now()
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

    def serialize_item(self):
        item = {
            "aid":self.aid,
            "nickname":self.aid.user.nickname,
            "cid":self.cid,
            "number":self.number,
            "price":self.price,
            "create_at":self.create_at
        }
        return item

    def get_purchase_curriculums(self,page=1,number=10):
        if page ==None:
            page = 1
        if number ==None:
            number = 10

        items = {}
        list_item = []

        shops = self.query.filter_by(aid=self.aid).paginate(int(page),int(number),False)
        for shop in shops.items:
            list_item.append(shop._curriculum.serialize_item())

        items["datas"] = list_item
        items["len"] = len(shops.items)
        items["nexts"] = shops.pages
        items["total"] = shops.total

        return items



    def get_days_shop_effective_sum(self,day):
        sql = """
        select 
        date_format(s.create_at,'%Y-%m-%d %H:%i:%S')as dateDay,sum(s.price)as moneyDay 
        FROM shopping_carts as s 
        group by dateDay 
        order by dateDay desc limit 0,{}      
        """.format(day)

        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items

    def get_month_shop_effective_sum(self,month):
        sql = """
        select 
        date_format(s.create_at,'%Y-%m')as dateMonth,sum(s.price)as moneyMonth 
        FROM shopping_carts as s 
        group by dateMonth
        order by dateMonth desc limit 0,{}      
        """.format(month)

        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items

    def get_monerys(self):
        sql = """
        select sum(s.price)as moneys FROM shopping_carts as s 
        """
        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items[0]