# 📚 Redis Library

Welcome to the **Redis Library**! This library provides utilities and tools to integrate Redis into your projects seamlessly. 🎉

## 📂 Project Structure

Here’s an overview of the project structure:

```
├── README.md
├── poetry.lock
├── pyproject.toml
└── src
    └── redis_lib
        ├── __init__.py
        ├── connection
        │   ├── __init__.py
        │   └── redis_connection.py
        ├── redis_handler.py
        ├── run.py
        └── start_form
            ├── __init__.py
            └── start_form.py
```

This structure includes a new `session` module, which contains the `session_handler.py` file for managing Redis sessions.
## 📥 Installation
To include this library in your project using Poetry, add it as a dependency in your `pyproject.toml` file:
```toml
[tool.poetry.dependencies]
redis-lib = { git = "https://github.com/renatoramossilva/redis-lib.git", rev = <release> }
```

Then, run the following command to install the dependency:
```bash
poetry install
```

## 🛠️ Usage
Here’s a quick example of how to use the library in your Python project:

```python
from connection.redis_connection import RedisConnectionHandler
from redis_handler import RedisHandler

redis_conn = RedisConnectionHandler().connect()
redis_repo = RedisHandler(redis_conn)

# Test the connection
if redis_conn.ping():
    print("🎉 Redis is connected!")
else:
    print("Unable to connect to Redis.")
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
      - "8001:8001"   # RedisInsight (web)
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

Enjoy using the Redis Library! 🚀
