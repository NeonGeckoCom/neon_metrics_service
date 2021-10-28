# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2021 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

import os
import time

from pprint import pformat
from os import makedirs
from os.path import join, expanduser, isdir
from neon_utils.logger import LOG

LOG_DIR = expanduser(os.getenv("NEON_METRICS_DIR", "~/.local/share/neon/metrics"))
if not isdir(LOG_DIR):
    LOG.info(f"Creating metrics logging directory at: {LOG_DIR}")
    makedirs(LOG_DIR)


def log_client_connection(log_file: str = None, **kwargs):
    log_file = expanduser(log_file or join(LOG_DIR, "connections.log"))
    with open(log_file, "a+") as log:
        log.write(f'{kwargs["time"]},{kwargs["ver"]},{kwargs["name"]},{kwargs["host"]}\n')


def log_metric(logs_dir: str = None, **kwargs):
    metric_to_log_name = {"failed-intent": "missed_intents.log",
                          "diagnostics": "sent_diagnostics.log",
                          "converse": "converse.log",
                          }
    log_file = metric_to_log_name.get(kwargs.get("name", ""), "metrics.log")
    logs_dir = expanduser(logs_dir or LOG_DIR)
    log_file = join(logs_dir, log_file)

    if not isdir(logs_dir):
        makedirs(logs_dir)

    # TODO: Add utterance timing metric emit/handling
    if kwargs.get("name") == "failed-intent":
        LOG.info("Intent Failure reported!")
        with open(log_file, "a+") as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{kwargs.get("device")},{kwargs.get("utterance")}\n')
    elif kwargs.get("name") == "diagnostics":  # TODO: This should probably have it's own handler DM
        LOG.info("Diagnostics Uploaded!")
        host = kwargs.get("host")
        uploaded = time.strftime("%Y-%m-%d_%H-%M-%S")
        upload_dir = join(logs_dir, "uploaded", f"{uploaded}__{host}")

        try:
            makedirs(upload_dir)
            # Write status
            with open(join(upload_dir, "status.log"), "a+") as status_log:
                status_log.write(kwargs.get("status"))
                status_log.write("\n")
            # Write configurations
            for key, val in kwargs.get("configurations").items():
                try:
                    with open(join(upload_dir, key), "a+") as file:
                        file.write(pformat(val))
                        file.write("\n")
                except Exception as e:
                    LOG.error(e)
                    LOG.debug(kwargs.get("configurations"))
            # Write transcripts
            if kwargs.get("transcripts"):
                try:
                    with open(join(upload_dir, "transcripts.csv"), "a+") as transcripts:
                        transcripts.write(kwargs.get("transcripts"))
                        transcripts.write("\n")
                except Exception as e:
                    LOG.error(e)
                    LOG.debug(kwargs.get("transcripts"))
            # Write logs
            if kwargs.get("logs"):
                for key, val in kwargs.get("logs").items():
                    try:
                        with open(join(upload_dir, f"{key}.log"), "a+") as file:
                            file.write(val)
                            file.write("\n")
                    except Exception as x:
                        LOG.error(key)
                        LOG.error(x)
        except Exception as e:
            LOG.error(e)
    elif kwargs.get("name") == "converse":
        with open(log_file, "a+") as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{kwargs.get("skill")},{kwargs.get("time")}\n')
    else:
        LOG.info("other metric reported")
        with open(log_file, "a+") as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{kwargs}\n')
