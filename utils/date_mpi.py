#!/usr/bin/env python3
"""This script updates Mongo record 'created' to 'Date' format."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import logging
import sys
from datetime import datetime
from pymongo.errors import ConnectionFailure

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def date_mpi(record_ids, funt_collection):
    """When the 'created' date is created in Mongo, it is a str. This function changes the
    MongoDB type to 'Date'. This is required for a MongoDB index job that purges older
    records. This index job is from managing the size of the Mongo database.

    Args:
        record_ids (int): MongoDB record object _id to check
        funt_collection (str): MongoDB connection string
    """
    logging.info("Entered date_mpi module.")

    for value in record_ids:
        record_id = {"_id": value}
        rec = funt_collection.find_one(record_id)
        date_string = rec["created"]
        try:
            if isinstance(date_string, datetime):
                logging.info("%s['created'] is already datetime.", value)
            else:
                mydate = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
                date_change = funt_collection.update_one(
                    {"_id": value}, {"$set": {"created": mydate}}
                )
                logging.info(
                    "%s['created'] type updated: %s", value, date_change.acknowledged
                )
        except ConnectionFailure as key_error:
            print(key_error)

    logging.info("Exited date_mpi module.")

    return
