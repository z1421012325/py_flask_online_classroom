# 假设服务器yum,python3.x版本,pip3,git 配置完整

# 下载虚拟环境包
pip3 install virtualenv

mkdir code && cd code

# 如果指定python版本请加参数-p python安装地址,例如
# virtualenv -p /usr/local/python3.6/bin/python3.6 venv
# 创建并激活虚拟环境
virtualenv venv && source venv/bin/activate

# 下载项目 注意配置ssh...
git clone git@github.com:z1421012325/py_flask_online_classroom.git

# 进入项目并下载依赖和gunicorn托管flask_web应用
cd py_flask_online_classroom
pip3 install -r requirements.txt && pip3 install gunicorn

# 托管
gunicorn -w 4 -b 0.0.0.1:9001 run:app

