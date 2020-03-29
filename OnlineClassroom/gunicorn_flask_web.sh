# 下载gunicorn
pip install gunicorn

# 开启4个线程 和开启flask_web的9001端口
gunicorn -w 4 -b 0.0.0.1:9001 run:app