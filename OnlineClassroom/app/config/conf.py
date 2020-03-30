# coding=utf-8
import os
import configparser

# 环境变量加载
def load_env():
    env_dist = os.environ
    return env_dist

# 配置文件加载
def read_ini():
    conf = configparser.ConfigParser()
    return conf.read("config.ini")


def init_db_url():
    # db_username = load_env().get("MYSQL_DB_USERNAME","root")
    # db_password = load_env().get("MYSQL_DB_PASSWORD","zyms90bdcs")
    # db_port     = load_env().get("MYSQL_DB_PORT","localhost")
    # db_host     = load_env().get("MYSQL_DB_HOST","3306")
    # db_dataname = load_env().get("MYSQL_DATABASE_NAME","online_lassroom")  # 这里写错了.. 实际为online_classroom

    db_username = read_ini().get("mysql","MYSQL_DB_USERNAME")
    db_password = read_ini().get("mysql","MYSQL_DB_PASSWORD")
    db_port     = read_ini().get("mysql","MYSQL_DB_PORT")
    db_host     = read_ini().get("mysql","MYSQL_DB_HOST")
    db_dataname = read_ini().get("mysql","MYSQL_DATABASE_NAME")

    sql_address = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(db_username,db_password,db_port,
    db_host,db_dataname)
    # return "mysql+pymysql://root:zyms90bdcs@localhost:3306/login"
    # return "mysql+mysqlconnector://root:zyms90bdcs@localhost:3306/login"
    return sql_address


class config():
    DEBUG           = False
    TESTING         = False

    SECRET_KEY      = read_ini().get("flask","SECRET_KEY")  # .format(os.urandom(10))

    # 是否开启wtf表单 防范csrf攻击
    WTF_CSRF_ENABLED = False
    # 返回json字符串为utf-8
    JSON_AS_ASCII = True

    # 数据库操作时是否显示原始SQL语句
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = read_ini().get("flask","SQLALCHEMY_POOL_SIZE")
    SQLALCHEMY_MAX_OVERFLOW =read_ini().get("flask","SQLALCHEMY_MAX_OVERFLOW")

    # email
    MAIL_SERVER     = read_ini().get("email","MAIL_SERVER")
    MAIL_PORT       = read_ini().get("email","MAIL_PORT")
    MAIL_USE_SSL    = True
    MAIL_USE_TLS    = False
    MAIL_USERNAME   = read_ini().get("email","MAIL_USERNAME")
    MAIL_PASSWORD   = read_ini().get("email","MAIL_PASSWORD")

    # 阿里云oss密钥
    ACCESS_KEY_ID = read_ini().get("aliyun","ACCESS_KEY_ID")
    ACCESS_KEY_SECRET = read_ini().get("aliyun","ACCESS_KEY_SECRET")
    # 地域节点
    ENDPOINT = read_ini().get("aliyun","ENDPOINT")
    # oss容器名称
    BUCKET_NAME = read_ini().get("aliyun","BUCKET_NAME")


class DeBugConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = init_db_url()


class TestConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = init_db_url()


# 上线生产环境
class ProducConfig(config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = init_db_url()


env = {
    "a":DeBugConfig,
    "b":TestConfig,
    "c":ProducConfig
}