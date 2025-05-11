"""
A RabbitMQ consumer wrapper for handling message consumption with a callback.
This module provides a RabbitMQ consumer class that allows consuming messages from a given queue.
"""

from typing import Any, Callable, Optional

import pika

import bindl.rabbitmq_wrapper.common


class RabbitmqConsumer(
    bindl.rabbitmq_wrapper.common.RabbitMQBase
):  # pylint: disable=too-few-public-methods
    """
    A RabbitMQ consumer class for consuming messages from a specified queue.
    This class uses the pika library to handle the connection and message consumption.
    """

    def __init__(
        self,
        queue: str,
        callback: Callable[..., Any],
        **kwargs: Optional[str],
    ) -> None:
        """
        Initializes a RabbitMQ consumer.

        **Parameters:**
            callback: The function to be called when a message is received.
            queue: The name of the RabbitMQ queue to consume messages from.
            host: The hostname of the RabbitMQ server. Defaults to "localhost".
            port: The port number of the RabbitMQ server. Defaults to 5672.
        """

        super().__init__(**kwargs)
        self.__queue = queue
        self.__callback = callback
        self.__connection_parameters = (self._create_connection(),)
        self.__channel = self.__create_channel()

    def __create_channel(self) -> pika.adapters.blocking_connection.BlockingChannel:
        """
        Creates a channel for consuming messages from RabbitMQ.

        **Parameters:**
            connection_parameters: The connection parameters for RabbitMQ.
        **Returns:**
            A channel object for consuming messages.
        """
        channel = pika.BlockingConnection(self.__connection_parameters).channel()
        channel.queue_declare(queue=self.__queue, durable=True)
        channel.basic_consume(
            queue=self.__queue, auto_ack=True, on_message_callback=self.__callback
        )

        return channel

    def start(self) -> None:
        """
        Starts consuming messages from the RabbitMQ queue.
        This method will block and listen for incoming messages.
        """
        print(f"Listen RabbitMQ queue: {self.__queue}")
        print("Waiting for messages...")
        self.__channel.start_consuming()
