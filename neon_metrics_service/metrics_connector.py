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

import pika.channel

from typing import Optional
from neon_utils import LOG
from neon_utils.socket_utils import b64_to_dict, dict_to_b64
from neon_mq_connector.connector import MQConnector

from neon_metrics_service.metrics_utils import log_metric, log_client_connection


class NeonMetricsConnector(MQConnector):
    """Adapter for establishing connection between Neon API and MQ broker"""

    def __init__(self, config: Optional[dict], service_name: str):
        """
            Additionally accepts message bus connection properties

            :param config: dictionary containing MQ configuration data
            :param service_name: name of the service instance
        """
        super().__init__(config, service_name)
        self.vhost = '/neon_metrics'

    @staticmethod
    def handle_record_metric(**kwargs):
        try:
            log_metric(**kwargs)
            return {"success": True}
        except Exception as e:
            LOG.error(e)
            return {"success": False}

    @staticmethod
    def handle_record_connection(**kwargs):
        try:
            log_client_connection(**kwargs)
            return {"success": True}
        except Exception as e:
            LOG.error(e)
            return {"success": False}

    def handle_metric(self,
                      channel: pika.channel.Channel,
                      method: pika.spec.Basic.Deliver,
                      _: pika.spec.BasicProperties,
                      body: bytes):
        """
            Handles input requests from MQ to Neon API

            :param channel: MQ channel object (pika.channel.Channel)
            :param method: MQ return method (pika.spec.Basic.Deliver)
            :param _: MQ properties (pika.spec.BasicProperties)
            :param body: request body (bytes)
        """
        message_id = None
        try:
            if body and isinstance(body, bytes):
                request = b64_to_dict(body)
                message_id = request.get("message_id")
                response = self.handle_record_metric(**request)
                response["message_id"] = message_id
                data = dict_to_b64(response)

                # queue declare is idempotent, just making sure queue exists
                channel.queue_declare(queue='neon_metrics_output')

                channel.basic_publish(exchange='',
                                      routing_key=request.get('routing_key', 'neon_metrics_output'),
                                      body=data,
                                      properties=pika.BasicProperties(expiration='1000')
                                      )
                channel.basic_ack(method.delivery_tag)
            else:
                raise TypeError(f'Invalid body received, expected: bytes string; got: {type(body)}')
        except Exception as e:
            LOG.error(f"message_id={message_id}")
            LOG.error(e)

    def handle_new_connection(self,
                              channel: pika.channel.Channel,
                              method: pika.spec.Basic.Deliver,
                              _: pika.spec.BasicProperties,
                              body: bytes):
        """
            Handles input requests from MQ to Neon API

            :param channel: MQ channel object (pika.channel.Channel)
            :param method: MQ return method (pika.spec.Basic.Deliver)
            :param _: MQ properties (pika.spec.BasicProperties)
            :param body: request body (bytes)
        """
        message_id = None
        try:
            if body and isinstance(body, bytes):
                request = b64_to_dict(body)
                message_id = request.get("message_id")
                self.handle_record_connection(**request)
                channel.basic_ack(method.delivery_tag)
            else:
                raise TypeError(f'Invalid body received, expected: bytes string; got: {type(body)}')
        except Exception as e:
            LOG.error(f"message_id={message_id}")
            LOG.error(e)

    def handle_error(self, thread, exception):
        LOG.error(f"{exception} in {thread}")
        LOG.info(f"Restarting Consumers")
        self.stop_consumers()
        self.run()

    def pre_run(self, **kwargs):
        self.register_consumer("neon_connections_consumer", self.vhost, 'neon_connections_input',
                               self.handle_new_connection, auto_ack=False)
        self.register_consumer("neon_metrics_consumer", self.vhost, 'neon_metrics_input',
                               self.handle_metric, auto_ack=False)
