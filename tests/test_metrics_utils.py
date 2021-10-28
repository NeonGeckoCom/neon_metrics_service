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
import shutil
import sys
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_metrics_service.metrics_utils import *

LOG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_logs")


class TestClientUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.makedirs(LOG_DIR)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(LOG_DIR)

    def test_log_connection(self):
        log_time = str(time.time())
        log_client_connection(join(LOG_DIR, "connections.txt"),
                              time=log_time, ver="0000.00.00", name="FriendlyName", host="HostName")
        with open(join(LOG_DIR, "connections.txt")) as f:
            self.assertTrue(f.readlines([-1] == ",".join((log_time, "0000.00.00", "FriendlyName", "HostName"))))

    def test_metrics(self):
        # TODO: Test cases for all metric messages (failed-intent, diagnostics, converse, other) DM
        pass


if __name__ == '__main__':
    unittest.main()
