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
        self.__connection_parameters = self._get_connection_params()
        self.__connection = self.__create_connection()
        self.__channel = self.__create_channel()

    def __declare_exchange(
        self, channel, exchange_type="direct", durable=True, auto_delete=False
    ):
        """
        Declares an exchange on the given RabbitMQ channel to ensure it exists.

        **Parameters:**
            channel: The RabbitMQ channel on which the exchange will be declared.
            exchange_type: The type of the exchange (e.g., 'direct', 'fanout', 'topic', 'headers').
                Defaults to 'direct'.
            durable: If True, the exchange will survive a broker restart.
            auto_delete: If True, the exchange will be deleted when no longer in use.

        Notes:
            - The exchange name is retrieved from the instance's `__exchange` attribute.
        """
        # Declare the exchange with additional control parameters
        channel.exchange_declare(
            exchange=self.__exchange,
            exchange_type=exchange_type,
            durable=durable,
            auto_delete=auto_delete,
        )

    def __create_channel(
        self,
        exchange_type: Optional[str] = "direct",
        durable: Optional[bool] = True,
        auto_delete: Optional[bool] = False,
    ) -> pika.adapters.blocking_connection.BlockingChannel:
        """
        Creates a channel for publishing messages to RabbitMQ and ensures the exchange exists.

        **Parameters:**
            exchange_type: The type of the exchange (e.g., 'direct', 'fanout', 'topic', 'headers').
            durable: If True, the exchange will survive a broker restart.
            auto_delete: If True, the exchange will be deleted when no longer in use.

        **Returns:**
            A channel object for publishing messages.

        **Raises:**
            RuntimeError: If the exchange cannot be declared.
        """
        channel = self.__connection.channel()
        try:
            # Declare the exchange to ensure it exists
            self.__declare_exchange(
                channel, exchange_type, durable=durable, auto_delete=auto_delete
            )
        except pika.exceptions.AMQPError as e:
            raise RuntimeError(
                f"Failed to declare exchange '{self.__exchange}': {e}"
            ) from e
        return channel

    def __create_connection(self) -> pika.BlockingConnection:
        """
        Creates a connection to RabbitMQ with error handling and retry logic.

        **Returns:**
            A BlockingConnection object for RabbitMQ.

        **Raises:**
            RuntimeError: If the connection to RabbitMQ cannot be established.
        """
        try:
            connection = pika.BlockingConnection(self.__connection_parameters)
            if not connection.is_open:
                raise RuntimeError("Failed to establish a connection to RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            raise RuntimeError(f"Error connecting to RabbitMQ: {e}") from e

    def send_message(self, body: Dict, mandatory: bool = False) -> None:
        """
        Sends a message to the specified exchange and routing key.

        **Parameters:**
            body: The message body to be sent. It should be a dictionary.
            mandatory: If True, raises an exception if the message cannot be routed to a queue.

        **Raises:**
            RuntimeError: If the message cannot be routed or delivered.
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
