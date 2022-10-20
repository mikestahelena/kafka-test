import json

from confluent_kafka import Producer
import socket
from datetime import datetime
from order_data_generator import fake_order_generator

import time

# https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html
# https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
producer = Producer(
    {
        "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
        "client.id": socket.gethostname(),
    }
)
topic = "customer-order"


def acked(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print(f"Failed to deliver message: {str(msg)}: {str(err)}")
    else:
        print(
            f"{datetime.now()} - "
            f"Message produced: topic: {str(msg.topic())}, "
            f"partition: {str(msg.partition())}, "
            f"offset: {str(msg.offset())}"
        )


if __name__ == "__main__":
    events = 0
    for p in fake_order_generator():
        producer.produce(
            topic,
            key=json.dumps({"cnpj": p["restaurant"]}, indent=4, ensure_ascii=False),
            value=json.dumps(p, indent=4, ensure_ascii=False),
            callback=acked,
        )
        # Wait up to 1 second for events. Callbacks will be invoked during
        # this method call if the message is acknowledged.
        events += producer.poll(1)
        time.sleep(0.1)
    producer.flush()
    print(f"All {events} messages sent")
