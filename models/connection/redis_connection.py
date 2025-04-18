"""This module provides a handler for managing Redis database connections."""

from typing import Optional, TypedDict

from redis import Redis


class RedisConnectionConfig(TypedDict):
    """Configuration for Redis connection."""

    HOST: str
    PORT: int
    DB: int


REDIS_CONNECTION_CONFIG: RedisConnectionConfig = {
    "HOST": "localhost",
    "PORT": 6379,
    "DB": 0,
}


class RedisConnectionError(Exception):
    """Custom exception for Redis connection errors."""


class RedisConnectionHandler:
    """
    Handles Redis database connections and provides methods to connect and retrieve the connection.
    """

    def __init__(self) -> None:
        """
        Handle Redis database connections.

        **Attributes:**
        - `host`: The hostname of the Redis server.
        - `port`: The port number of the Redis server.
        - `db`: The database number to connect to.
        - `connection`: The Redis connection object (initialized as None).

        **Methods:**
        - `connect()`: Establish a connection to the Redis server.
        - `get_connection()`: Retrieve the active Redis connection. Raises an exception
        if the connection is not established.
        """
        self.__host: str = REDIS_CONNECTION_CONFIG["HOST"]
        self.__port: int = REDIS_CONNECTION_CONFIG["PORT"]
        self.__db: int = REDIS_CONNECTION_CONFIG["DB"]
        self.__connection: Optional[Redis] = None

    def connect(self) -> Redis:
        """
        Establish a connection to the Redis database.

        **Returns:**
        - `Redis`: An instance of the Redis connection.
        """
        self.__connection = Redis(host=self.__host, port=self.__port, db=self.__db)
        return self.__connection

    def get_connection(self) -> Redis:
        """
        Retrieve the established Redis connection.

        **Details:**
        - Ensures that a connection to the Redis database has been established.
        - Raises an exception if the connection is not yet initialized.

        **Returns:**
        - `Redis`: The active Redis connection instance.

        **Raises:**
        - `Exception`: If the connection has not been established by calling `connect()`.
        """
        if self.__connection is None:
            raise RedisConnectionError(
                "Connection not established. Call connect() first."
            )
        return self.__connection
