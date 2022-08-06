#!/usr/bin/env python3
"""This script responds to requestor with invalid CVE format notification."""

__author__ = "Aaron Davis"
__version__ = "0.1.5"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import configparser
import logging
import json
import os
import sys
import requests


KEY = "CI"
if os.getenv(KEY):
    webex_bearer = os.environ["webex_bearer"]
else:
    config = configparser.ConfigParser()
    config.read(r".\config.ini")
    webex_bearer = config["WEBEX"]["bearer"]

webex_msg_url = "https://webexapis.com/v1/messages"
webex_token = f"Bearer {webex_bearer}"
webex_headers = {"Authorization": webex_token, "Content-Type": "application/json"}

# Formatted message using markdown markup language
# (https://developer.webex.com/docs/basics#formatting-messages)
DEFAULT_MSG_BODY = """
**Invalid CVE request format.**

CVE request should be "CVE-[4-digit year]-[4 or more digits]"

For example: CVE-2022-20816

Please resubmit request."""


def invalid_notify(ids, funt_collection):
    """This function tests for valid CVE format in request.

    Args:
        ids (int): MongoDB record object _id of invalid sub requests
        funt_collection (str): MongoDB connection string

    Returns:
        bad_cve (list): List of record _id with invalid format
        good_cve (list): List of record _id with valid format
    """
    logging.info("Entered invalid_notify module.")

    # Respond to invalid requests
    for _ in ids:
        record_id = {"_id": _}
        collect = funt_collection.find_one(record_id)
        room_id = collect["roomId"]
        webex_payload = json.dumps({"roomId": room_id, "markdown": DEFAULT_MSG_BODY})
        if "invalid_cve" not in collect:
            try:
                response = requests.request(
                    "POST", webex_msg_url, headers=webex_headers, data=webex_payload
                )
                status_code = response.status_code
                funt_collection.update_one({"_id": _}, {"$set": {"invalid_cve": True}})
                logging.warning("Invalid CVE message sent status: %s", status_code)
            except requests.HTTPError:
                if status_code in (401, 403):
                    logging.error("Invalid Webex API key.")
                elif status_code == 404:
                    logging.error("Invalid Webex resource requested (%s).", status_code)
                elif status_code == 429:
                    logging.error(
                        "Webex API calls per minute exceeded (%s).", status_code
                    )
                elif status_code >= 500:
                    logging.error(
                        "Something went horribly wrong with the Webex server (%s).",
                        status_code,
                    )
                sys.exit(1)
        else:
            logging.info("Invalid CVE request record already marked.")

    logging.info("Exited invalid_notify module.")

    return
