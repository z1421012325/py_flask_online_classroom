# coding=utf-8

from .OnlineClassroom.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
