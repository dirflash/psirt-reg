#!/usr/bin/env python3
"""This script checks for duplicate subscription requests."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import logging
import sys
from deepdiff import DeepDiff

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def dup_chk(record_ids, funt_collection):
    """This function is testing for duplicate subscription requests. If a duplicate is found,
    a "dup_request" record is added to the MongoDB document.

    Args:
        record_ids (int): MongoDB record object _id to check
        funt_collection (str): MongoDB connection string

    Returns:
        (list): List of record _id deemed to be duplicate requests.
    """
    logging.info("Entered dup_chk module.")
    logging.info("Before duplicate test: %s", len(record_ids))
    dupl_chk = []
    dup_record = []
    subs = []
    for cnt, value in enumerate(record_ids):
        record_id = {"_id": value}
        dup_collect = funt_collection.find_one(record_id)
        if "dup_request" in dup_collect:
            dup_record.append(value)
        else:
            subs.append(value)
        dupl_chk.append(
            {
                "record_id": value,
                "created": dup_collect["created"],
                "personId": dup_collect["personId"],
                "msg_txt": dup_collect["text"],
            }
        )
    cnt_rng = cnt + 1
    ddiff_list = []
    for i in range(cnt_rng):
        for e in range(i + 1, cnt_rng):
            ddiff = DeepDiff(
                dupl_chk[i],
                dupl_chk[e],
                exclude_paths={"root['record_id]", "root['created']"},
            )
            if bool(ddiff) is False:
                ddiff_list.append(dupl_chk[e]["record_id"])
    for ri in ddiff_list:
        logging.info("Checking %s.", ri)
        if ri not in dup_record:
            dup_req = funt_collection.update_one(
                {"_id": ri},
                {"$set": {"dup_request": True}},
            )
            if ri in subs:
                ri_pop = subs.index(ri)
                subs.pop(ri_pop)
            logging.info("%s['dup_request'] added: %s", ri, dup_req.acknowledged)
        else:
            logging.info("%s['dup_request'] already added.", ri)
    post_record_ids = len(record_ids) - len(ddiff_list)
    logging.info("After duplicate test: %s", post_record_ids)

    logging.info("Exited dup_chk module.")

    return subs
