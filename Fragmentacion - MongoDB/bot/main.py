from crud import create, read, update, delete
from datetime import datetime
from time import sleep
from random import choice

CRUD_CHOICE = [create, read, update, delete]

while True:
    sleep(2)
    option = choice(CRUD_CHOICE)

    try:
        res = option()
    except Exception as e:
        res = "[ERROR]" + str(e)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now + " " + res)
    with open("bot.log", "a+") as file:
        file.write(now + " " + res + "\n")
        file.close()
