# coding=utf-8

from flask import Flask,jsonify

from OnlineClassroom.app.config import conf
from OnlineClassroom.app.ext import plugins


def create_app():
    app = Flask(__name__)

    # 配置加载
    app.config.from_object(conf.env.get("a","b"))

    # 插件加载
    plugins.ext_init(app)

    # 蓝图加载...
    from OnlineClassroom.app.views import registry_blue
    registry_blue.init_blue(app)





    # err handler 处理
    @app.errorhandler(500)
    def app_500_err_res(err):
        print(err)
        return jsonify({"code":50001,"msg":"500 bad not found"})

    @app.errorhandler(404)
    def app_404_err_res(err):
        print(err)
        return jsonify({"code":40001,"msg":"404 bad not found"})

    @app.errorhandler(405)
    def app_500_err_res(err):
        print(err)
        return jsonify({"code": 40005, "msg": "405 bad not found"})

    return app