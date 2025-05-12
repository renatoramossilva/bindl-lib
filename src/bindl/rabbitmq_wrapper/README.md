# ![RabbitMQ](https://upload.wikimedia.org/wikipedia/commons/7/71/RabbitMQ_logo.svg) Wrapper

## 📖 Overview

This repository provides two modules for interacting with RabbitMQ: a consumer wrapper and a publisher wrapper. Both modules leverage the `pika` library to simplify RabbitMQ operations.

## 🛠️ RabbitMQ Consumer Module

The `RabbitmqConsumer` class simplifies the process of consuming messages from a RabbitMQ queue.

- 🔌 Connects to a RabbitMQ server with customizable host and port.
- 📥 Consumes messages from a specified queue.
- 🛠️ Allows users to define a custom callback function for processing incoming messages.

## 🚀 RabbitMQ Publisher Module

The `RabbitmqPublisher` class enables sending messages to a RabbitMQ exchange with a specified routing key.

- 📤 Publishes messages to a RabbitMQ exchange.
- 🗂️ Supports specifying routing keys for message delivery.
- 📝 Handles JSON-encoded message bodies.
- ⚙️ Configurable RabbitMQ server host and port.

# 🐳 Running RabbitMQ with Docker

To run RabbitMQ locally during development or testing, you can use either Docker or Docker Compose.

### Option 1: Using Docker CLI
```bash
docker run -d --name rabbitmq \
    -p 5672:5672 \
    -p 15672:15672 \
    -e RABBITMQ_USER=$RABBITMQ_USER \
    -e RABBITMQ_PASS=$RABBITMQ_PASS \
    rabbitmq:3-management
```

This command runs RabbitMQ in a Docker container with the management interface enabled.

- 🔑 **5672** is the default port for AMQP protocol.
- 🌐 **15672** is used for accessing the RabbitMQ web management UI.

Access the web UI at [http://localhost:15672](http://localhost:15672).

### Option 2: Using Docker Compose
Create a `docker-compose.yml` file in your project root:

```yaml
services:
    rabbitmq:
        image: rabbitmq:3-management
        container_name: rabbitmq
        ports:
            - "5672:5672"
            - "15672:15672"
        environment:
            RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
            RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS}
```

Start RabbitMQ with:

```bash
docker-compose up -d
```


## 🧑‍💻 Using the RabbitMQ Wrapper

### RabbitMQ Publisher Example

To publish messages to a RabbitMQ exchange, use the `RabbitmqPublisher` class as shown below:

```python
import bindl.rabbitmq_wrapper.publisher as pub

# Initialize the RabbitMQ publisher
rabbitmq_publisher = pub.RabbitmqPublisher(<exchange_name>)

# Send a message
rabbitmq_publisher.send_message(dict(<payload>))
```

### RabbitMQ Consumer Example

To consume messages from a RabbitMQ queue, use the `RabbitmqConsumer` class and define a callback function to process incoming messages:

```python
import bindl.rabbitmq_wrapper.consumer as con

# Define a callback function to process messages
def my_callback(ch, method, properties, body):
    print(body)

# Initialize the RabbitMQ consumer
rabitmq_consumer = con.RabbitmqConsumer(
    queue="queue_test",
    callback=my_callback,
)

# Start consuming messages
rabitmq_consumer.start()
```

### Example with Routing Key

#### RabbitMQ Publisher with Routing Key

```python
import bindl.rabbitmq_wrapper.publisher as pub

# Initialize the RabbitMQ publisher with a routing key
rabbitmq_publisher = pub.RabbitmqPublisher(
    exchange=<exchange-name>,
    routing_key=<routing-key_name>,
)

# Send a message with the specified routing key
rabbitmq_publisher.send_message(dict(<payload>))
```

#### RabbitMQ Consumer for Specific Queue

```python
import bindl.rabbitmq_wrapper.consumer as con

# Define a callback function to process messages
def my_callback(ch, method, properties, body):
    print(body)

# Initialize the RabbitMQ consumer for a specific queue
rabitmq_consumer = con.RabbitmqConsumer(
    queue=<queue_name>,
    callback=my_callback,
)

# Start consuming messages
rabitmq_consumer.start()
```

These simple examples demonstrate how to use the RabbitMQ wrapper for publishing and consuming messages in your application.
