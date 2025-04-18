# 🚀 Redis Playground

Welcome to the **Redis Playground**! This guide will help you set up and explore Redis quickly and efficiently. 🎉

## 📥 Install Redis
To install Redis on your system, run the following command:
```bash
brew install redis
```

## 🖥️ Install Another Redis Desktop Manager
For a graphical interface to manage Redis, install **Another Redis Desktop Manager**:
```bash
brew install --cask another-redis-desktop-manager
```

## 🐳 Run Redis with Docker
Spin up a Redis container using Docker:
```bash
docker run -d --name redis-container -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

## 🧪 Test Your Redis Setup
Verify your Redis setup with the following Python code:
```python
from redis import Redis

# Connect to Redis
r = Redis("localhost", 6379, 0)

# Test the connection
if r.ping():
    print("🎉 Redis is running!")
else:
    print("❌ Unable to connect to Redis.")
```

## 🌐 Access Redis GUI
You can access the Redis GUI by navigating to the following URL in your browser:

[http://localhost:8001/](http://localhost:8001/)

## 🐋 Run Redis with Docker Compose
Alternatively, you can use Docker Compose to set up Redis. Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'
services:
    redis:
        image: redis/redis-stack:latest
        container_name: redis-compose-container
        ports:
            - "6379:6379"
            - "8001:8001"
```

Then, start the Redis service with:
```bash
docker compose up -d
```

To stop the service, use:
```bash
docker compose down
```

Enjoy exploring Redis! 🚀