from pymongo import MongoClient
from random import choice
import json

# DATABASE SETTINGS
URI = "mongodb://127.0.0.1:27017/"
CLIENT = MongoClient(URI)
DATABASE = CLIENT["shardDB"]

# DATA
NAMES = json.loads(open("data\\names.json").read())
SURNAMES = json.loads(open("data\\surnames.json").read())


def _get_random_data():
    return {
        "name": choice(NAMES).get("name"),
        "surname": choice(SURNAMES).get("surname"),
    }

def crud_method(callback):
    def function():
        table = DATABASE.people
        data = _get_random_data()
        return callback(data, table)
    return function


@crud_method
def create(data, table):
    table.insert_one(data)
    return "[CREATE] %s %s Created successfully" %(data["name"], data["surname"])

@crud_method
def read(data, table):
    res = table.find_one(data)
    return "[READ] %s" %(res or "%s Not Found" %data)


@crud_method
def update(data, table):
    new_data = _get_random_data()
    res = table.update_one(data, {"$set": new_data})
    message = "[UPDATE] %s Modified Documents" %res.modified_count
    message += "(%s -> %s)" %(data, new_data) if res.modified_count else "(%s)" %data
    return message


@crud_method
def delete(data, table):
    res = table.delete_one(data)
    message = None
    if not res.deleted_count:
        message = "[DELETE] %s %s Satisfactorily eliminated" %(data["name"], data["surname"])
    else:
        message = "[DELETE] %s %s Not found" %(data["name"], data["surname"])
    return message



