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
        self.__connection_parameters = self._get_connection_params()
        self.__connection = self.__create_connection()
        self.__channel = self.__create_channel(self.__connection)

    def __create_connection(self) -> pika.BlockingConnection:
        """
        Creates a connection to RabbitMQ.

        **Returns:**
            A connection object to RabbitMQ.
        """
        try:
            return pika.BlockingConnection(self.__connection_parameters)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while creating the connection: {e}")
            raise

    def __create_channel(
        self, connection: pika.BlockingConnection
    ) -> pika.BlockingConnection.channel:
        """
        Creates a channel for consuming messages from RabbitMQ.

        **Parameters:**
            connection: The RabbitMQ connection object.

        **Returns:**
            A channel object for consuming messages.
        """
        try:
            channel = connection.channel()
            channel.queue_declare(queue=self.__queue, durable=True)
            channel.basic_qos(prefetch_count=1)  # Ensures fair dispatch of messages
            channel.basic_consume(
                queue=self.__queue, auto_ack=True, on_message_callback=self.__callback
            )
            return channel
        except pika.exceptions.ChannelError as e:
            print(f"Failed to create a channel: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while creating the channel: {e}")
            raise

    def start(self) -> None:
        """
        Starts consuming messages from the RabbitMQ queue.
        This method will block and listen for incoming messages.
        """
        try:
            print(f"Listening to RabbitMQ queue: {self.__queue}")
            print("Waiting for messages...")
            self.__channel.start_consuming()
        except KeyboardInterrupt:
            print("\nConsumption interrupted by user. Closing connection...")
        except Exception as e:  # pylint: disable=broad-except
            print(f"An error occurred while consuming messages: {e}")
        finally:
            if self.__channel.is_open:
                self.__channel.close()
            if self.__connection.is_open:
                self.__connection.close()
            print("Connection closed.")
