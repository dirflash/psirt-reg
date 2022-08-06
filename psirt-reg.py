#!/usr/bin/env python3
"""This script is the logic and brains for psirt-bot subscriptions."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import configparser
import logging
import os
import sys
import json
import requests
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.dup_chk import dup_chk
from utils.date_mpi import date_mpi
from utils.cve_chk import cve_chk
from utils.invalid_notify import invalid_notify

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

logging.info("--- Start run ---")

new_record = collection.find({"sub": {"$exists": False}})

# Get the new record ID's in Mongo
pre_record_ids = [rec.get("_id") for rec in new_record]

# Update 'created' format to 'Date'
date_mpi(pre_record_ids, collection)

# Check for duplicate subscription requests
subscription = dup_chk(pre_record_ids, collection)

invalid_cve, valid_cve = cve_chk(subscription, collection)
print(invalid_cve)
print(valid_cve)

if len(invalid_cve) > 0:
    invalid_notify(invalid_cve, collection)

logging.info("--- End run ---")
