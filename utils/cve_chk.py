#!/usr/bin/env python3
"""This script checks for valid CVE format in requests."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import logging
import re


def cve_chk(subs, funt_collection):
    """This function tests for valid CVE format in request.

    Args:
        subs (int): MongoDB record object _id of non-duplicated sub requests
        funt_collection (str): MongoDB connection string

    Returns:
        bad_cve (list): List of record _id with invalid format
        good_cve (list): List of record _id with valid format
    """
    logging.info("Entered sub_chk module.")

    bad_cve = []
    good_cve = []

    for value in subs:
        record_id = {"_id": value}
        sub_collect = funt_collection.find_one(record_id)
        cve_string = sub_collect["text"]
        cve_test = re.search(
            "[cC][vV][eE]-20[1-2][0-9]-[0-9][0-9][0-9][0-9]+", cve_string
        )
        if bool(cve_test) is False:
            bad_cve.append(value)
        else:
            good_cve.append(value)
        logging.info("%s matches CVE format: %s", value, bool(cve_test))

    logging.info("%s invalid cve format.", len(bad_cve))
    logging.info("Exited cve_chk module.")

    return (bad_cve, good_cve)
