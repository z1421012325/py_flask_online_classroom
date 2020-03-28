# coding=utf-8



from .user.v1.handlers.user import user
from .user.v1.handlers.curriculum import curriculum_
from .user.v1.handlers.teacher import teacher
from .user.v1.handlers.search import search

from .admin import admin

def init_blue(app):

    # 面向用户
    app.register_blueprint(blueprint=user,url_prefix='/user')
    app.register_blueprint(blueprint=curriculum_, url_prefix='/curriculum')
    app.register_blueprint(blueprint=teacher, url_prefix='/teacher')
    app.register_blueprint(blueprint=search)

    # 后台api
    app.register_blueprint(blueprint=admin,url_prefix="/admin")