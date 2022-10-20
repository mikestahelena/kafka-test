import json
import uuid

from confluent_kafka import Consumer

# https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html
# https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
        "group.id": "customer-order-consumers",
        "client.id": f"consumer-{uuid.uuid4()}",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
        "partition.assignment.strategy": "cooperative-sticky",
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
                # print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print(f"error: {msg.error()}")
            else:
                # Check for Kafka message
                print(
                    f"Topic: {msg.topic()} - Partition : {msg.partition()} - Offset : {msg.offset()}"
                )
                record_key = "Null" if msg.key() is None else msg.key().decode("utf-8")
                record_value = json.loads(msg.value().decode("utf-8"))

                order_items = record_value['items']
                for item in order_items:
                    print(f"Pedido: {record_value['id']} - item: {item['item']} - {item['dish']} com {item['spices']} e {item['vegetable']} com {item['fruit']} + bebida {item['drink']}")

    except KeyboardInterrupt:
        pass
    finally:
        print("Leave group and commit final offsets")
        consumer.close()
