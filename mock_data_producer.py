import time
import random
import uuid
from datetime import datetime
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

# Callback function to report delivery status
def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred, or None on success.
        msg (Message): The message that was produced or failed.
    """
    if err is not None:
        print(f"❌ Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"✅ Record {msg.key()} produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    print("====================================")

# Kafka and Schema Registry configuration
kafka_config = {
    'bootstrap.servers': '--Add your Kafka bootstrap servers here--',
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'add your username here',
    'sasl.password': '--add your password here',
}

schema_registry_client = SchemaRegistryClient({
    'url': 'add your schema registry URL here',
    'basic.auth.user.info': 'add your schema registry username here:--add your schema registry password here'
})

key_serializer = StringSerializer('utf_8')

# Fetch the latest Avro schema from Schema Registry
def get_latest_schema(subject):
    schema = schema_registry_client.get_latest_version(subject).schema.schema_str
    return AvroSerializer(schema_registry_client, schema)

# Kafka producers for orders and payments
orders_producer = SerializingProducer({
    **kafka_config,
    'key.serializer': key_serializer,
    'value.serializer': get_latest_schema('macd_orders-value')
})

payments_producer = SerializingProducer({
    **kafka_config,
    'key.serializer': key_serializer,
    'value.serializer': get_latest_schema('macd_payments-value')
})

# Sample McDonald's menu items
menu_items = [
    "Big Mac", "McChicken", "Quarter Pounder", "French Fries", "McFlurry",
    "Filet-O-Fish", "Chicken McNuggets", "Egg McMuffin", "Hash Browns", "Apple Pie"
]

# Function to generate and stream mock order/payment data
def generate_orders_and_payments():
    utc_now = int(datetime.utcnow().timestamp() * 1000)

    for _ in range(500):
        order_id = str(uuid.uuid4())
        customer_id = f"cust_{random.randint(10000, 99999)}"
        order_total = round(random.uniform(10, 100), 2)
        order_time = utc_now - random.randint(0, 24 * 60 * 60 * 1000)

        order_items = [
            {
                "item_name": random.choice(menu_items),
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(1, 10), 2)
            }
            for _ in range(random.randint(1, 3))
        ]

        payment_id = str(uuid.uuid4())
        payment_amount = order_total
        payment_method = random.choice(["credit_card", "debit_card", "cash", "mobile_payment"])
        payment_time = order_time + random.randint(0, 5 * 60 * 1000)

        # Produce to orders topic
        orders_producer.produce(
            topic='macd_orders',
            key=order_id,
            value={
                "order_id": order_id,
                "customer_id": customer_id,
                "order_total": order_total,
                "order_items": order_items,
                "order_time": order_time
            },
            on_delivery=delivery_report
        )
        orders_producer.flush()

        # Produce to payments topic
        payments_producer.produce(
            topic='macd_payments',
            key=payment_id,
            value={
                "payment_id": payment_id,
                "order_id": order_id,
                "payment_amount": payment_amount,
                "payment_method": payment_method,
                "payment_time": payment_time
            },
            on_delivery=delivery_report
        )
        payments_producer.flush()

        time.sleep(2)

# Run the mock data generation
if __name__ == "__main__":
    generate_orders_and_payments()
    print("✅ Mock data successfully published.")
