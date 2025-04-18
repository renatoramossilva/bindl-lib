"""Redis Test"""

from models.connection.redis_connection import RedisConnectionHandler
from models.redis_handler import RedisHandler

redis_conn = RedisConnectionHandler().connect()
redis_repo = RedisHandler(redis_conn)
print(redis_repo)

print("Setting value in Redis")
redis_repo.set_value("foo", "bar")
print("Done")
print("Getting value from Redis")
print(redis_repo.get_value("foo"))
print("Done2")
# print("Deleting value from Redis")
# redis_repo.delete_key("foo")
# print("Done3")
