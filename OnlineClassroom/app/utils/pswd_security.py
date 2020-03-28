# coding=utf-8

from werkzeug.security import check_password_hash,generate_password_hash



def encryption(pswd,salt_length=None):
    if salt_length == None:
        return generate_password_hash(pswd)
    return generate_password_hash(password=pswd,salt_length=salt_length)

def check_pswd(now,input):
    if len(now) == 0 or input == None:
        return False
    return check_password_hash(now, input)


if __name__ == '__main__':
    print(encryption("1234567890"))