"""Load all cache data on the start form"""

from typing import Any, Dict, Optional

from redis_lib.connection.redis_connection import RedisConnectionHandler
from redis_lib.redis_handler import RedisHandler


class _StartForm:
    """
    A class to manage a cache of data with optional retrieval by key.
    """

    def __init__(self) -> None:
        """
        Initialize the StartForm object.
        **Attributes:**
        - `__cache_date`: An optional dictionary to store cached data.
        It is initialized as `None` and can hold key-value pairs of any type.
        """
        self.__cache_date: dict[str, Any] = {}

        redis_conn = RedisConnectionHandler().connect()
        redis_repo = RedisHandler(redis_conn)
        keys = redis_conn.keys("*")

        for key in keys:  # type: ignore
            key = key.decode("utf-8")
            value = redis_repo.get_value(key)
            if value:
                self.__cache_date[key] = value
        self.load_cache(self.__cache_date)

    def load_cache(self, data: Dict[str, Any]) -> None:
        """
        Load data into the cache.
        **Parameters:**
        - `data`: A dictionary containing key-value pairs to be loaded into the cache.
        """
        self.__cache_date = data

    def get_cache(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache using the specified key.
        **Parameters:**
        - `key`: The key to look up in the cache.
        **Returns:**
        - The value associated with the key if it exists in the cache, otherwise `None`.
        """

        if self.__cache_date and key in self.__cache_date:
            return self.__cache_date[key]
        return None


start_form = _StartForm()
