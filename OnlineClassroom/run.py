# coding=utf-8

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from OnlineClassroom.app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

def cmd_host_debug_option():
    port = 0
    debug = False
    option_config = ""

    argvs = sys.argv
    for index,argv in  enumerate(argvs[1:]):
        if "-debug" in argv:
            debug = True
        if "-p" in argv:
            input = argvs[index+2]
            try:
                _port = int(input)
            except ValueError as v:
                port = 5000
            else:
                port = _port
        if "-config" in argv:  # a-debug,b-test,c-production分别为开发,测试,生产,如果其他参数,config配置默认为debug模式
            option_config = str(argvs[index + 2])
    return debug,port,option_config

if __name__ == "__main__":
	# debug,test cmd:"python run.py -p 9999 -debug -config a" or b
	# python run.py 端口随机,默认为生产环境
    debug,port,option = cmd_host_debug_option()
	
    if option == "":
        option = "c"   # 默认生产环境
	
    app = create_app(option)
    app.run(host="0.0.0.0", port=port, debug=debug)

    # manage = Manager(app=app)
    # manage.add_command("db", MigrateCommand)
    # manage.run()
    # python run.py runserver

	# gunicron 托管则不需要设置host,port,由gunicorn启动wsgi网关