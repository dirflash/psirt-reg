#!/usr/bin/env python3
"""This script checks for valid CVE format in requests."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import logging
import sys
import re


def cve_chk(subs, funt_collection):
    """This function is testing for duplicate subscription requests. If a duplicate is found,
    a "dup_request" record is added to the MongoDB document.

    Args:
        record_ids (int): MongoDB record object _id to check
        funt_collection (str): MongoDB connection string

    Returns:
        (list): List of record _id deemed to be duplicate requests.
    """
    logging.info("Entered sub_chk module.")

    for value in subs:
        record_id = {"_id": value}
        sub_collect = funt_collection.find_one(record_id)
        cve_string = sub_collect["text"]
        cve_test = re.search(
            "[cC][vV][eE]-20[1-2][0-9]-[0-9][0-9][0-9][0-9]+", cve_string
        )
        logging.info("%s matches CVE format: %s", value, bool(cve_test))

    logging.info("Exited cve_chk module.")

    return
