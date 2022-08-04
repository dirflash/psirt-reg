#!/usr/bin/env python3
"""This script checks for rapid requests."""

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
    logging.info("Before duplicate test: %s", len(record_ids))
    dupl_chk = []
    for cnt, value in enumerate(record_ids):
        record_id = {"_id": value}
        dup_collect = funt_collection.find_one(record_id)
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
                ddiff_list.append(e)
    dup_ids = [dupl_chk[d]["record_id"] for d in ddiff_list]
    for i in dup_ids:
        funt_collection.update_one(
            {"_id": i},
            {"$set": {"dup_request": True}},
        )
    post_record_ids = len(record_ids) - len(dup_ids)
    logging.info("After duplicate test: %s", post_record_ids)

    return dup_ids