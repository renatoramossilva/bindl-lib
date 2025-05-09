# 📚 Redis Wrapper

<img src="https://www.svgrepo.com/show/303460/redis-logo.svg" alt="Redis Logo" width="100"/>

**Redis Wrapper** is a lightweight Python wrapper that provides utilities and tools to integrate Redis into your projects seamlessly. 🎉

## 📂 Wrapper Structure

Here’s an overview of the wrapper structure:

```
├── __init__.py
├── connection
│   ├── __init__.py
│   └── redis_connection.py
├── redis_handler.py
└── start_form
    ├── __init__.py
    └── start_form.py
```

This structure includes the `connection` module, which contains the `redis_connection.py` file for managing Redis sessions.

## 🛠️ Usage
Here’s a quick example of how to use the library in your Python project:

```python
import bindl.redis_wrapper.connection.redis_connection as rc
import bindl.redis_wrapper.redis_handler as rh

redis_conn = rc.RedisConnectionHandler().connect()
redis_repo = rh.RedisHandler(redis_conn)

# Test the connection
if redis_conn.ping():
    print("🎉 Redis is connected!")
else:
    print("Unable to connect to Redis.")

redis_repo.set_value("foo2", "bar2")

print("Getting value from Redis")
print(redis_repo.get_value("foo2"))
```

## 🐳 Running Redis Locally
If you need a local Redis instance for development, you can use Docker to spin up a container:
```bash
docker run -d --name redis-container -p 6379:6379 redis/redis-stack:latest
```

## 🐋 Run Redis with Docker Compose
Alternatively, you can use Docker Compose to set up Redis. Create a `docker-compose.yml` file with the following content:

```yaml
services:
  redis:
    container_name: redis-container
    image: redis/redis-stack:latest
    ports:
      - "6379:6379"
      - "8001:8001"   # RedisInsight (WEB)
    restart: unless-stopped
```

Then, start the Redis service with:
```bash
docker compose up -d
```

To stop the service, use:
```bash
docker compose down
```

Enjoy using the Redis wrapper! 🚀
