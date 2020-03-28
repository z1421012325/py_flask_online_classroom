# coding=utf-8


import uuid



def get_uuid():
    id = uuid.uuid4().hex

    return id




if __name__ == '__main__':
    get_uuid()
