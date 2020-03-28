# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()


# 第三方插件初始化
def ext_init(app):
    CORS(app)
    db.init_app(app)
    Migrate(app=app,db=db)

