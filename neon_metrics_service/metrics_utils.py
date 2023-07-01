# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
import json

from pprint import pformat
from os import makedirs
from os.path import join, expanduser, isdir
from ovos_utils.log import LOG

_LOG_DIR = None


def get_log_dir():
    global _LOG_DIR
    if not _LOG_DIR:
        if os.getenv("NEON_METRICS_DIR"):
            LOG.info(f"Got log directory from env: "
                     f"{os.getenv('NEON_METRICS_DIR')}")
            _LOG_DIR = expanduser(os.getenv("NEON_METRICS_DIR"))
        else:
            from ovos_utils.xdg_utils import xdg_data_home
            LOG.info(f"Using default XDG path: {xdg_data_home()}")
            _LOG_DIR = join(xdg_data_home(), "neon", "metrics")
    if not isdir(_LOG_DIR):
        LOG.info(f"Creating metrics logging directory at: {_LOG_DIR}")
        makedirs(_LOG_DIR)
    return _LOG_DIR


def log_client_connection(log_file: str = None, **kwargs):
    log_file = expanduser(log_file or join(get_log_dir(), "connections.log"))
    with open(log_file, "a+") as log:
        log.write(f'{kwargs["time"]},{kwargs["ver"]},{kwargs["name"]},'
                  f'{kwargs["host"]}\n')


def log_metric(logs_dir: str = None, **kwargs):
    metric_to_log_name = {"failed-intent": "missed_intents.log",
                          "diagnostics": "sent_diagnostics.log",
                          "converse": "converse.log",
                          }
    log_file = metric_to_log_name.get(kwargs.get("name", ""), "metrics.log")
    logs_dir = expanduser(logs_dir or get_log_dir())
    log_file = join(logs_dir, log_file)

    if not isdir(logs_dir):
        makedirs(logs_dir)

    # TODO: Add utterance timing metric emit/handling
    if kwargs.get("name") == "failed-intent":
        LOG.info("Intent Failure reported!")
        with open(log_file, "a+") as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},'
                      f'{kwargs.get("device")},{kwargs.get("utterance")}\n')
    # TODO: This should probably have it's own handler DM
    elif kwargs.get("name") == "diagnostics":
        LOG.info("Diagnostics Uploaded!")
        host = kwargs.get("host")
        uploaded = time.strftime("%Y-%m-%d_%H-%M-%S")
        upload_dir = join(logs_dir, "uploaded", f"{uploaded}__{host}")

        try:
            makedirs(upload_dir)
            # Write startup log
            if kwargs.get("startup"):
                with open(join(upload_dir, "startup.log"), "a+") as startup_log:
                    startup_log.write(kwargs.get("startup"))
                    startup_log.write("\n")
            # Write configurations
            if kwargs.get("configurations"):
                configurations = kwargs["configurations"]
                if isinstance(configurations, str):
                    configurations = json.loads(kwargs["configurations"])
                for key, val in configurations.items():
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
                    with open(join(upload_dir,
                                   "transcripts.csv"), "a+") as transcripts:
                        transcripts.write(kwargs.get("transcripts"))
                        transcripts.write("\n")
                except Exception as e:
                    LOG.error(e)
                    LOG.debug(kwargs.get("transcripts"))
            # Write logs
            if kwargs.get("logs"):
                logs = kwargs["logs"]
                if isinstance(logs, str):
                    logs = json.loads(logs)
                for key, val in logs.items():
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
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},'
                      f'{kwargs.get("skill")},{kwargs.get("time")}\n')
    else:
        LOG.info("other metric reported")
        with open(log_file, "a+") as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{kwargs}\n')
