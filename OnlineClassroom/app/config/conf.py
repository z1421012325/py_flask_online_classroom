# coding=utf-8
import os


def load_env():
    env_dist = os.environ
    return env_dist


def init_db_url():
    db_username = load_env().get("MYSQL_DB_USERNAME","root")
    db_password = load_env().get("MYSQL_DB_PASSWORD","zyms90bdcs")
    db_port     = load_env().get("MYSQL_DB_PORT","localhost")
    db_host     = load_env().get("MYSQL_DB_HOST","3306")
    db_dataname = load_env().get("MYSQL_DB_PASSWORD","online_lassroom")

    sql_address = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(db_username,db_password,db_port,
    db_host,db_dataname)
    # return "mysql+pymysql://root:zyms90bdcs@localhost:3306/login"
    # return "mysql+mysqlconnector://root:zyms90bdcs@localhost:3306/login"
    return sql_address


class config():
    DEBUG           = False
    TESTING         = False

    SECRET_KEY      = 'SD15DFG1G4D231X86HF1GDSF{}cxCV156DSRFCVDFG'  # .format(os.urandom(10))



    # 是否开启wtf表单 防范csrf攻击
    WTF_CSRF_ENABLED = False

    # 数据库操作时是否显示原始SQL语句
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW =50
    # email
    MAIL_SERVER     = 'smtp.qq.com'
    MAIL_PORT       = 465
    MAIL_USE_SSL    = True
    MAIL_USE_TLS    = False
    MAIL_USERNAME   = load_env().get("EMAIL_USERNAME","'1421012325@qq.com'")
    MAIL_PASSWORD   = load_env().get("EMAIL_PASSWORD","'osmxjrjphhydjfcj'")

    # 阿里云oss密钥
    ACCESS_KEY_ID = "LTAI4FtjynxBKcAmF9JKtGDs"
    ACCESS_KEY_SECRET = "LeWv80kDekE4HYSg0CQzsznlyv3h8S"
    # 地域节点
    ENDPOINT = "oss-cn-shenzhen.aliyuncs.com"
    # oss容器名称
    BUCKET_NAME = "demo-online-classroom"


class DevelopConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = init_db_url()


class TestConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = init_db_url()


# 上线生产环境
class ProducConfig(config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = init_db_url()


env = {
    "a":DevelopConfig,
    "b":TestConfig,
    "c":ProducConfig
}