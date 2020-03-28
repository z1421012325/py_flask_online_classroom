# coding=utf-8

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from OnlineClassroom.app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

app=create_app()

manage = Manager(app=app)
manage.add_command("db",MigrateCommand)


if __name__ == "__main__":
    manage.run()
    # python run.py runserver

    # app.run(host="0.0.0.0",debug=False)