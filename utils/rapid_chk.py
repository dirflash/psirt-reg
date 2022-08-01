#!/usr/bin/env python3
"""This script checks for rapid requests."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def rapid_chk(record_ids, funt_collection):
    logging.info("Before rapid request filter: %s", record_ids)
    for cnt, value in enumerate(record_ids):
        record_id = {"_id": value}
        dup_collect = funt_collection.find_one(record_id)
        record_count = cnt + 1
    return record_count


"""

pre_record_ids = [rec.get("_id") for rec in new_record]

dup_check = []
for count, value in enumerate(record_ids):
    record_id = {"_id": value}
    dup_collect = collection.find_one(record_id)
    created = dup_collect["createdAt"]
    email = dup_collect["Email"]
    dup_check.append({"record_id": record_id, "msg_created": created, "email": email})

LEN_DUP_CHECK = len(dup_check)

for x in reversed(range(LEN_DUP_CHECK)):
    logging.info("Duplicate primary check index: %s", x)
    source_dup_check = dup_check[x]["record_id"]["_id"]
    source_e_compare = dup_check[x]["email"]
    source_m_compare = dup_check[x]["msg_created"]
    if isinstance(source_m_compare, str):
        update_created(source_dup_check, source_m_compare)
    source_lookup = collection.find_one(record_id)
    source_m_converted = source_lookup["createdAt"]
    sec_dup_check = x - 1
    logging.info("Duplicate compare check index: %s", sec_dup_check)
    if sec_dup_check >= 0:
        secondary_dup_check = dup_check[sec_dup_check]["record_id"]["_id"]
        sec_e_compare = dup_check[sec_dup_check]["email"]
        sec_m_compare = dup_check[sec_dup_check]["msg_created"]
        if isinstance(sec_m_compare, str):
            update_created(secondary_dup_check, sec_m_compare)
        sec_lookup = collection.find_one(record_id)
        sec_m_converted = sec_lookup["createdAt"]
        if source_e_compare == sec_e_compare:
            logging.info("Duplicate email address found.")
            record_delta = source_m_converted - sec_m_converted
            logging.info("Compare messages record delta: %s", record_delta)
            if record_delta < timedelta(seconds=10):
                print("within threshold - not a good message")
                logging.info("Duplicate message sent less than 10 seconds.")
                tagged_msg_id = record_ids[x]
                logging.info("Tag msg id  %s as duplicate.", tagged_msg_id)
                try:
                    dup_msg_id = record_ids[x]
                    collection.update_one(
                        {"_id": dup_msg_id},
                        {"$set": {"response": "duplicate"}},
                    )
                    record_ids.pop(x)
                except ConnectionFailure as update_err:
                    logging.exception(update_err)
            else:
                print("exceeded threshold - send good message")
"""
# end rapid request filter
