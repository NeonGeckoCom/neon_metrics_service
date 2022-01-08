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
