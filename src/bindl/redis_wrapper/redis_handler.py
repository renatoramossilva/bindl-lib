"""A module for handling Redis database operations, including key-value and hash operations."""

from typing import Any, Optional


class RedisHandler:
    """
    A handler class for interacting with a Redis database. Provides methods for
    direct key-value operations and hash operations.

    **Attributes:**
    - `redis`: An instance of the Redis client.
    """

    def __init__(self, redis_conn) -> None:
        """
        Initialize the RedisHandler with the specified Redis server connection details.

        **Request Body:**
        - `host`: The hostname of the Redis server. Defaults to 'localhost'.
        - `port`: The port number of the Redis server. Defaults to 6379.
        - `db`: The database index to connect to. Defaults to 0.
        """
        self.__redis_conn = redis_conn

    # Direct key-value operations
    def set_value(self, key: str, value: Any, expiration: Optional[int] = None) -> None:
        """
        Set a key-value pair in the Redis database.

        **Request Body:**
        - `key`: The key to set.
        - `value`: The value to associate with the key.
        - `expiration`: The expiration time in seconds (optional).
        If not provided, the key will not expire.
        """
        try:
            self.__redis_conn.set(key, value, ex=expiration)
        except Exception as e:
            raise RuntimeError(
                f"Failed to set key '{key}' with value '{value}': {e}"
            ) from e

    def get_value(self, key: str) -> str | None:
        """
        Retrieve the value associated with a given key from the Redis database.

        **Request Body:**
        - `key`: The key to retrieve the value for.

        **Returns:**
        A string containing the value associated with the key, or `None` if the key does not exist.
        """
        try:
            value = self.__redis_conn.get(key)
            return value.decode("utf-8") if isinstance(value, bytes) else None
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve value for key '{key}': {e}") from e

    def delete_key(self, key: str) -> None:
        """
        Delete a key-value pair from the Redis database.

        **Request Body:**
        - `key`: The key to delete.
        """
        try:
            self.__redis_conn.delete(key)
        except Exception as e:
            raise RuntimeError(f"Failed to delete key '{key}': {e}") from e

    # Hash operations
    def set_hash(
        self, name: str, key: str, value: str, expiration: Optional[int] = None
    ) -> None:
        """
        Set a field in a hash stored in the Redis database.

        **Request Body:**
        - `name`: The name of the hash.
        - `key`: The field key within the hash.
        - `value`: The value to associate with the field key.
        - `expiration`: The expiration time in seconds (optional).
        If not provided, the hash will not expire.
        """
        try:
            self.__redis_conn.hset(name, key, value)
            if expiration:
                self.__redis_conn.expire(name, expiration)
        except Exception as e:
            raise RuntimeError(
                f"Failed to set hash '{name}' with key '{key}' and value '{value}': {e}"
            ) from e

    def get_hash(self, name: str, key: str) -> str | None:
        """
        Retrieve the value of a field in a hash from the Redis database.

        **Request Body:**
        - `name`: The name of the hash.
        - `key`: The field key within the hash.

        **Returns:**
        A string containing the value associated with the field key, or `None`
        if the field does not exist.
        """
        try:
            value = self.__redis_conn.hget(name, key)
            return value.decode("utf-8") if isinstance(value, bytes) else None
        except Exception as e:
            raise RuntimeError(
                f"Failed to retrieve hash '{name}' with key '{key}': {e}"
            ) from e
