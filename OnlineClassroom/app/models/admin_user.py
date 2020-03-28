# coding=utf-8

import datetime
from OnlineClassroom.app.ext.plugins import db

from OnlineClassroom.app.utils.pswd_security import *

# 内部员工表
"""
create table admins_user (
`aid` int primary key auto_increment comment '内部员工id',
`username` char(20) not null comment '账号',
`pswd` varchar(255) not null comment '密码',
`status` tinyint default '0' comment '身份状态 0为未激活,1激活成功可使用,9离职(其他)',
`create_at` datetime default now(),
`r_id` int comment '权限id',
CONSTRAINT `role_id` FOREIGN KEY (`r_id`) REFERENCES `admin_roles` (`r_id`),
)ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;


密码经过加密 原始密码为 1234567890
insert into admins_user (username,pswd,status,r_id) values ('boss','pbkdf2:sha256:150000$vqMjaptw$1326cfd6afdc0425af4690011bd0af1db470a316a801d9b4b2c20f25c65e82a7',1,9)
"""

class Admin_Users(db.Model):
    __tablename__ = "admins_user"
    aid = db.Column(db.Integer,primary_key=True,comment="内部员工id")
    username = db.Column(db.String(20),comment="账号")
    pswd = db.Column(db.String(255),comment="密码")
    status = db.Column(db.Integer,comment="身份状态 0为未激活,1激活成功可使用,9离职(其他)")  # tinyint
    create_at = db.Column(db.DateTime,default=datetime.datetime.now())
    r_id = db.Column(db.Integer,db.ForeignKey("admin_roles.r_id"),comment="权限id")



    status_lever_1 = 0
    status_lever_2 = 1
    status_lever_3 = 9

    default_pswd = "1234567890"

    def __repr__(self):
        return "数据库{}".format(self.__tablename__)

    def __init__(self,aid=None,username=None,pswd=None,status=None,r_id=None):
        self.aid = aid
        self.username = username
        if status == None:
            self.pswd = self.default_pswd
        if status == None:
            self.status = self.status_lever_1
        self.create_at = datetime.datetime.now()
        if r_id:
            self.r_id = 1

    def serializetion_json(self):
        item = {
            "aid" : self.aid,
            "username" : self.username,
            "status" : self.status ,
            "ct" : self.exis_time_is_null(),
            "rid" : self.r_id
        }
        return item

    def exis_time_is_null(self):
        if self.create_at == None:
            return ""
        return self.create_at.strftime("%Y-%m-%d %H:%M:%S")

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
        self.r_id if self.r_id == None else 1
        self.set_pswd(self.pswd)
        return self.is_commit()


    def get_user_activation(self):
        u = self.query.filter_by(username=self.username,status=self.status_lever_2).first()
        return u

    def get_user_unactivation(self):
        u = self.query.filter_by(username=self.username, status =self.status_lever_1).first()
        return u

    def get_user_aid_unactivation(self):
        u = self.query.filter_by(aid=self.aid, status=self.status_lever_1).first()
        return u
    def get_user_aid_activation(self):
        u = self.query.filter_by(aid=self.aid, status=self.status_lever_2).first()
        return u

    def check_login_user_pswd(self,input_pswd):
        u = self.get_user_activation()
        if u == None:
            return u,False
        return u,u.check_pswd(input_pswd)

    def modify_pswd(self,now_pswd):
        self.set_pswd(now_pswd)
        return self.up_commit()

    def exis_activation_user_status(self):
        list_status = [self.status_lever_2,self.status_lever_3,self.status_lever_1]
        return self.status in list_status

    def modift_auth_status(self,r_id):
        if int(r_id) not in [1,2,3]:
            return False
        if int(r_id) == self.r_id:
            return False
        self.r_id = r_id
        return self.up_commit()

    def get_unactivation_accounts(self,page=None,number=None,r_id=None):
        if page == None:
            page = 1
        if number == None:
            number = 10
        if r_id == None:
            r_id = 9
        elif r_id == 9:
            r_id = 10

        us = self.query.filter(Admin_Users.status==self.status_lever_1,Admin_Users.r_id<r_id).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for u in us.items:
            list_item.append(u.serializetion_json())

        items["datas"] = list_item
        items["pages"] = us.pages
        items["total"] = us.total
        items["len"] = len(us.items)

        return items

    def get_leave_accounts(self,page=None,number=None,r_id=None):
        if page == None:
            page = 1
        if number == None:
            number = 10
        if r_id == None:
            r_id = 1
        elif r_id == 9:
            r_id = 10

        us = self.query.filter(Admin_Users.status==self.status_lever_3,Admin_Users.r_id<r_id).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for u in us.items:
            list_item.append(u.serializetion_json())

        items["datas"] = list_item
        items["pages"] = us.pages
        items["total"] = us.total
        items["len"] = len(us.items)

        return items

    def get_all_accounts(self,page=None,number=None,r_id=None):
        if page == None:
            page = 1
        if number == None:
            number = 10
        if r_id == None:
            r_id = 1
        elif r_id == 9:
            r_id = 10
        us = self.query.filter(Admin_Users.status==self.status_lever_2,Admin_Users.r_id<r_id).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for u in us.items:
            list_item.append(u.serializetion_json())

        items["datas"] = list_item
        items["pages"] = us.pages
        items["total"] = us.total
        items["len"] = len(us.items)

        return items

    def get_all_unaccounts(self,page=None,number=None,r_id=None):
        if page == None:
            page = 1
        if number == None:
            number = 10
        if r_id == None:
            r_id = 1
        elif r_id == 9:
            r_id = 10

        us = self.query.filter(Admin_Users.status==self.status_lever_1,Admin_Users.r_id<r_id).paginate(int(page),int(number),False)

        items = {}
        list_item = []

        for u in us.items:
            list_item.append(u.serializetion_json())

        items["datas"] = list_item
        items["pages"] = us.pages
        items["total"] = us.total
        items["len"] = len(us.items)

        return items


    def exis_in_default_status(self):
        list_status = [self.status_lever_1,self.status_lever_2,self.status_lever_3]
        return self.status in list_status

    def set_status_lever1(self):
        self.status = self.status_lever_1
    def set_status_lever2(self):
        self.status = self.status_lever_2
    def set_status_lever3(self):
        self.status = self.status_lever_3
    def get_status_lever(self):
        return self.status
    def set_username(self,username):
        self.username = username
    def get_username(self):
        return self.username
    def set_create_At(self):
        self.create_at = datetime.datetime.now()
    def get_create_At(self):
        return self.create_at.strftime('%Y-%m-%d %H:%M:%S')

    def set_pswd(self,pswd):
        self.pswd = encryption(pswd)
    def check_pswd(self,input):
        return check_pswd(self.pswd,input)
    def get_rid(self):
        return self.r_id
    def set_rid(self,rid):
        self.r_id = rid
    def get_aid(self):
        return self.aid
    def set_aid(self):
        pass