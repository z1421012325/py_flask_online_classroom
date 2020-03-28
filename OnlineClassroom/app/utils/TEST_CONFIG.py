

from OnlineClassroom.app import create_app

print(create_app().config.get("ACCESS_KEY_ID"))
print(create_app().config.get("ACCESS_KEY_SECRET"))