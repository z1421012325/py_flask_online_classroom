# coding=utf-8

import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from OnlineClassroom.app.ext.plugins import db

from .extracts import Extracts
from .money import Money
from .purchases import Purchases
from .shopping_carts import ShoppingCarts
from .use_collections import Use_collections
from .curriculum_comments import CurriculumComments
from .curriculums import Curriculums

from OnlineClassroom.app.utils.pswd_security import *
from OnlineClassroom.app.utils.sql_result import sql_result_to_dict

"""
account

create table accounts (
    `aid` int primary key auto_increment comment '用户id',
    `nickname` char(20) not null comment '昵称',
    `username` char(20) not null comment '账号',
    `pswd` varchar(255) not null comment '密码',
    `status` tinyint default '0' comment '身份状态',
    `info` text comment '一些额外的信息',
    `create_at` datetime default now(),
    
    `admin_id` int comment '操作员工id',
    `open_at` datetime comment '操作时间'
    CONSTRAINT `admin_id` FOREIGN KEY (`admin_id`) REFERENCES `admins_user` (`aid`),
    
    UNIQUE KEY `nickname` (`nickname`),
    UNIQUE KEY `username` (`username`))
    ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;

"""


class Account(db.Model):

    __tablename__ = "accounts"

    aid         = db.Column(db.Integer,primary_key=True,comment="用户id")
    nickname    = db.Column(db.String(20),nullable=False,unique=True, comment="昵称")
    username    = db.Column(db.String(20),nullable=False,unique=True,comment="账号")
    pswd        = db.Column(db.String(255),nullable=False,comment="密码")
    status      = db.Column(db.Integer,comment="身份状态")
    info        = db.Column(db.TEXT,comment="一些额外的信息")
    create_at   = db.Column(db.DateTime,default=datetime.datetime.now(),comment="创建时间")

    admin_id   = db.Column(db.Integer,db.ForeignKey("admins_user.aid"),comment="操作员工id")
    open_at     = db.Column(db.DateTime,comment="操作时间")

    # sqlalchemy orm特有的关系条件,不存在数据库表中,只是在存在实例中
    # 第一个参数为对应模型的class类名,第二个参数在对应的类中生成一个属性,关联到这个表
    # 这种关系只存在 一对多的 '一' 中
    # PS 如果多个模型不在同一个文件中会发生错误,"找不到模型" 所以import 模型
    curriculum = db.relationship(Curriculums,backref="user", lazy="dynamic")
    comments = db.relationship(CurriculumComments,backref="user", lazy="dynamic")
    extracts = db.relationship(Extracts,backref="user", lazy="dynamic")
    money = db.relationship(Money,backref="user", lazy="dynamic")
    purchases = db.relationship(Purchases,backref="user", lazy="dynamic")
    shops = db.relationship(ShoppingCarts,backref="user", lazy="dynamic")
    use_collections = db.relationship(Use_collections, backref="_user", lazy="dynamic")

    DefaultUserAccountStatus     = 0       # 用户状态 0为未注册用户
    RegisteredUsersTeacherStatus = 1       # 注册用户(老師)
    RegisteredUsersStudentStatus = 2       # 注册用户(學生)
    BannedUsersStatus            = 10      # 封禁用户

    def __init__(self,nickname=None,username=None,pswd=None,info=None,aid=None):
        self.nickname = nickname
        self.username = username
        self.pswd = pswd
        self.status  = self.RegisteredUsersStudentStatus
        self.info = info
        self.aid=aid

    def __repr__(self):
        return "数据库{}  {} --- {} ----- {}".format(self.__tablename__,self.nickname,self.username,self.aid)



    def EncryptionPassword(self):
        self.pswd = encryption(self.pswd)       # 简单的加密,没有加盐值

    @classmethod
    def SetEncryptionPassword(self,pswd):
        return encryption(pswd)

    def CheckPassword(self,pswd):
        return check_pswd(self.pswd,pswd)




    # 学生注册
    def registryStudentAccount(self):
        self.EncryptionPassword()
        return self.is_commit()

    # 老师注册
    def registryTeacherAccount(self):
        self.status = self.RegisteredUsersTeacherStatus
        self.EncryptionPassword()
        return self.is_commit()

    # 修改信息
    def modify_user_info(self,nickname,info):
        if len(nickname) != 0:
            self.nickname = nickname
        if len(info) != 0:
            self.info = info

        return self.up_commit()



    # 修改密码
    def modify_pswd(self,old,new):
        if not self.CheckPassword(old):
            return False

        self.pswd = self.SetEncryptionPassword(new)

        return self.up_commit()


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


    # 是否为老师身份
    def is_UsersTeacherStatus(self):
        return self.status == self.RegisteredUsersTeacherStatus
    # 是否为学生身份
    def is_UsersStudentStatus(self):
        return self.status == self.RegisteredUsersStudentStatus


    def serializetion_item(self):
        item = {
            "aid": self.aid,
            "nickname": self.nickname,
            "username": self.username,
            "info": self.info,
            "status": self.status,
            "create_at": self.exis_time_is_null()
        }
        return item

    def exis_time_is_null(self):
        if self.create_at == None:
            return ""
        return self.create_at.strftime('%Y-%m-%d %H:%M:%S')

    def query_Teachers(self,page=1,number=10):
        if page == None :
            page = 1
        if number == None:
            number = 10

        teachers = self.query.filter_by(status=self.RegisteredUsersTeacherStatus).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for teacher in teachers.items:
            list_item.append(teacher.serializetion_item())

        items["datas"] = list_item
        items["len"] = len(teachers.items)
        items["nexts"] = teachers.pages
        items["total"] = teachers.total

        return items


    def get_aid_user_to_serializetion(self):
        u = self.query.filter(Account.aid==self.aid).first()
        return u.serializetion_item()

    def get_aid_user(self):
        u = self.query.filter(Account.aid==self.aid).first()
        return u

    def prohibit_user(self,admin_aid):
        u = self.get_aid_user()
        if u == None:
            return False
        u.status = self.BannedUsersStatus
        u.admin_id = admin_aid
        u.open_at = datetime.datetime.now()
        return u.up_commit()

    def reduction_prohibit_user(self,admin_aid):

        u = self.query.filter_by(aid=self.aid).first()
        if u == None:
            return False
        u.status = self.RegisteredUsersStudentStatus
        u.admin_id =admin_aid
        u.open_at = datetime.datetime.now()
        return u.up_commit()

    def get_prohibit_users(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        users = self.query.filter(Account.status == self.BannedUsersStatus).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for user in users.items:
            list_item.append(user.serializetion_item())

        items["datas"] = list_item
        items["len"] = len(users.items)
        items["nexts"] = users.pages
        items["total"] = users.total

        return items

    def get_aid_is_UsersTeacherStatus(self):
        u = self.query.filter_by(aid=self.aid).first()
        return u.is_UsersTeacherStatus()



    def get_day_registry_count(self,day=10):
        sql = "select " \
              "DAte_format(u.create_at,'%Y-%m-%d') as dateDay,count(*) as countDay " \
              "from accounts as u where u.status != 0 and u.status !=10 " \
              "group by dateDay order by dateDay desc " \
              "limit 0,{}".format(day)

        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items


    def get_registry_counts(self):
        sql = """
            select count(*) as count from accounts
        """
        results = db.session.execute(sql).fetchall()
        items = sql_result_to_dict(results)
        return items[0]


    def get_users(self,page=1,number=10):
        if page == None:
            page = 1
        if number == None:
            number = 10

        users = self.query.filter().paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for user in users.items:
            list_item.append(user.serializetion_item())

        items["datas"] = list_item
        items["len"] = len(users.items)
        items["nexts"] = users.pages
        items["total"] = users.total

        return items
