"""RabbitMQ Base Class for Publisher and Consumer"""

import os
from typing import Optional

import pika


class RabbitMQBase:  # pylint: disable=too-few-public-methods
    """
    Base class for RabbitMQ Publisher and Consumer.
    This class provides common connection and channel creation methods.
    It is not intended to be used directly.
    """

    def __init__(self, **kwargs: Optional[str]) -> None:
        """
        Initializes the RabbitMQ base class with connection parameters.
        """
        if os.getenv("RABBITMQ_USER") is None or os.getenv("RABBITMQ_PASS") is None:
            raise RuntimeError(
                "Environment variables RABBITMQ_USER and RABBITMQ_PASS must be set"  # noqa: E501
            )
        self.__host = kwargs.get("host") or "localhost"
        self.__port = kwargs.get("port") or 5672
        self.__username = kwargs.get("username") or os.getenv("RABBITMQ_USER")
        self.__password = kwargs.get("password") or os.getenv("RABBITMQ_PASS")

    def _create_connection(self) -> pika.BlockingConnection:
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username, password=self.__password
            ),
        )
        return connection_parameters
