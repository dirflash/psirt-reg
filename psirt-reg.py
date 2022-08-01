#!/usr/bin/env python3
"""This script is the logic and brains for psirt-bot scriptions."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import configparser
import logging
from datetime import datetime, date, timedelta, timezone
import os
import sys
import json
from time import time
import requests
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.rapid_chk import rapid_chk

# from utils import date_mip


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

KEY = "CI"
if os.getenv(KEY):
    mongoaddr = "cluster0.jzvod.mongodb.net"
    mongodb = "PSIRT"
    mongocollect = "subscriptions"
    mongouser = os.environ["mongouser"]
    mongopw = os.environ["mongopw"]
    webex_bearer = os.environ["webex_bearer"]
else:
    config = configparser.ConfigParser()
    config.read("config.ini")
    mongoaddr = config["MONGO"]["mongo_addr"]
    mongodb = config["MONGO"]["mongo_db"]
    mongocollect = config["MONGO"]["mongo_collect"]
    mongouser = config["MONGO"]["user_name"]
    mongopw = config["MONGO"]["password"]
    webex_bearer = config["WEBEX"]["bearer"]

MAX_MONGODB_DELAY = 500

Mongo_Client = MongoClient(
    f"mongodb+srv://{mongouser}:{mongopw}@{mongoaddr}/{mongodb}?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=MAX_MONGODB_DELAY,
)

db = Mongo_Client[mongodb]
collection = db[mongocollect]


def update_created(recerd, date_string):
    """When the 'createdAt' date is created in Mongo, it is a str. This function changes the
    MongoDB type to 'date'. This is required for a MongoDB index job that purges records
    older than 7-days. This index job is from managing the size of the Mongo database.

    Args:
        record (int): MongoDB record object _id
        date_string (str): The records created time to be converted
    """
    try:
        mydate = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        collection.update_one({"_id": recerd}, {"$set": {"createdAt": mydate}})
    except ConnectionFailure as key_error:
        print(key_error)


new_record = collection.find({"sub": {"$exists": False}})

# Get the new record ID's in Mongo

pre_record_ids = [rec.get("_id") for rec in new_record]

duplicate_collection = rapid_chk(pre_record_ids, collection)

print(duplicate_collection)
