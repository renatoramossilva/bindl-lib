"""Redis Test"""

from redis_lib.connection.redis_connection import RedisConnectionHandler
from redis_lib.redis_handler import RedisHandler
from redis_lib.start_form.start_form import start_form

redis_conn = RedisConnectionHandler().connect()
redis_repo = RedisHandler(redis_conn)
print(redis_repo)

print("Setting value in Redis")
redis_repo.set_value("foo2", "bar2")
print("Done")
print("Getting value from Redis")
print(redis_repo.get_value("foo2"))
print("Done2")

print("Getting value from cache")
print(start_form.get_cache("foo"))
print("Getting value from cache2")
print(start_form.get_cache("foo2"))
