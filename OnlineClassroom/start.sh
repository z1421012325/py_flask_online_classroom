# 下载虚拟环境virtualenv
pip install virtualenv

# 创建文件夹并进入
mkdir myproject
cd myproject

# 创建虚拟环境,名为 venv并进入创建的当前目录/venv/bin/activate使用source激活虚拟环境
virtualenv venv
source venv/bin/activate

# git下载项目到该目录并进入
git cloen git@github.com:z1421012325/py_flask_online_classroom.git
cd py_flask_online_classroom/OnlineClassroom

# 下载依赖库
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ 

# 启动
# chmod +x linux-run.sh
# ./linux-run.sh
# 由gunicron进行多线程启动
chmod +x gunicorn_flask_web.sh
./gunicorn_flask_web.sh

# 开启负载均衡nginx....



