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
    """When the 'createdAt' date is created in Mongo, it is a str. This function changes the
    MongoDB type to 'date'. This is required for a MongoDB index job that purges records
    older than 7-days. This index job is from managing the size of the Mongo database.

    Args:
        record (int): MongoDB record object _id
        date_string (str): The records created time to be converted
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
