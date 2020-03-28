# coding=utf-8

import datetime
from OnlineClassroom.app.ext.plugins import db
from .admin_user import Admin_Users

# 员工权限表
"""
角色
CREATE TABLE `admin_roles` (
  `r_id` int NOT NULL COMMENT '角色id,表示员工权限,1普通员工,2组长?,3主管,9老板-- 123都有增删改查权限.3能注册12权限员工,9(我全都要)',
  `r_name` char(10) DEFAULT '普通员工' COMMENT '角色名字'
) ENGINE=InnoDB DEFAULT CHARSET=utf8

insert into admin_roles (r_id,r_name) values (1,'普通员工')
insert into admin_roles (r_id,r_name) values (2,'组长')
insert into admin_roles (r_id,r_name) values (3,'主管')
insert into admin_roles (r_id,r_name) values (9,'boss')
"""


class admin_roles(db.Model):
    __tablename__ = "admin_roles"
    r_id = db.Column(db.Integer,primary_key=True,comment="角色id,表示员工权限,1普通员工,2组长?,3主管,9老板-- 123都有增删改查权限.3能注册12权限员工,9(我全都要)")
    r_name = db.Column(db.String(10), comment="角色名字")

    admin_users = db.relationship(Admin_Users, backref="role", lazy="dynamic")



    auth_lever1 = 1
    auth_lever2 = 2
    auth_lever3 = 3
    auth_lever4 = 9

    def __repr__(self):
        return "数据库{}".format(self.__tablename__)

    def __init__(self,r_id=None,r_name=None):
        self.r_id = r_id
        self.r_name = r_name if r_name == None else self.auth_lever1












    def get_rid(self):
        return self.r_id
    def set_rid(self):
        pass
    def set_name(self,name):
        self.r_name = name
    def get_name(self):
        return self.r_name



