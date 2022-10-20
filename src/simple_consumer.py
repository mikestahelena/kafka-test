import json

from confluent_kafka import Consumer

# https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html
consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "customer-order-consumers",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True
    }
)
topic = "customer-order"
consumer.subscribe([topic])

if __name__ == "__main__":
    try:
        while True:
            msg = consumer.poll(1)
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print(f"error: {msg.error()}")
            else:
                # Check for Kafka message
                print(
                    f"Connected to Topic: {msg.topic()} and Partition : {msg.partition()}"
                )
                record_key = "Null" if msg.key() is None else msg.key().decode("utf-8")
                record_value = json.loads(msg.value().decode("utf-8"))
                print(
                    f"Consumed record with key {record_key} and value {record_value} with Offset : {msg.offset()}"
                )
    except KeyboardInterrupt:
        pass
    finally:
        print("Leave group and commit final offsets")
        consumer.close()
