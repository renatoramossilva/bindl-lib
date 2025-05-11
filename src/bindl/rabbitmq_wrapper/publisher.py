"""
Publisher for RabbitMQ using pika library.
This module provides a RabbitMQ publisher class that allows
sending messages to a specified exchange and routing key.
"""

import json
from typing import Dict, Optional

import pika

import bindl.rabbitmq_wrapper.common


class RabbitmqPublisher(
    bindl.rabbitmq_wrapper.common.RabbitMQBase
):  # pylint: disable=too-few-public-methods
    """
    A RabbitMQ publisher class for sending messages to a specified exchange and routing key.
    This class uses the pika library to handle the connection and message publishing.
    """

    def __init__(
        self,
        exchange: str,
        routing_key: Optional[str] = "",
        **kwargs: Optional[str],
    ) -> None:
        """
        Initializes a RabbitMQ publisher.

        **Parameters:**
            exchange: The name of the RabbitMQ exchange to publish messages to.
            routing_key: The routing key for the message.
            host: The hostname of the RabbitMQ server. Defaults to "localhost".
            port: The port number of the RabbitMQ server. Defaults to 5672.
        """
        super().__init__(**kwargs)
        self.__exchange = exchange
        self.__routing_key = routing_key
        self.__connection_parameters = (self._create_connection(),)
        self.__channel = self.__create_channel()

    def __create_channel(self) -> pika.adapters.blocking_connection.BlockingChannel:
        """
        Creates a channel for publishing messages to RabbitMQ.

        **Parameters:**
            connection_parameters: The connection parameters for RabbitMQ.
        **Returns:**
            A channel object for publishing messages.
        """
        channel = pika.BlockingConnection(self.__connection_parameters).channel()
        return channel

    def send_message(self, body: Dict) -> None:
        """
        Sends a message to the specified exchange and routing key.

        **Parameters:**
            body: The message body to be sent. It should be a dictionary.
        """
        try:
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(delivery_mode=2),
                mandatory=mandatory,
            )
        except pika.exceptions.UnroutableError as e:
            raise RuntimeError(f"Message could not be routed: {e}") from e
        except pika.exceptions.NackError as e:
            raise RuntimeError(f"Message was not acknowledged: {e}") from e
