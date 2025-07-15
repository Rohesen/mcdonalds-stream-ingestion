
## ✅ Steps Overview

### 1. 🛠 Kafka Setup

* Provisioned Kafka cluster using **Confluent Cloud** in `ap-south-1`.
* Enabled **Schema Registry** and created two topics:

  * `macd_orders`
  * `macd_payments`

---

### 2. 🧪 Python Mock Data Generation

A Python script (`kafka_producer.py`) generates and publishes 500 mock orders and payments using Avro serialization.

#### 🧾 Sample Order Record

```json
{
  "order_id": "uuid",
  "customer_id": "cust_12345",
  "order_total": 52.30,
  "order_items": [
    {"item_name": "Big Mac", "quantity": 2, "price": 5.99}
  ],
  "order_time": 1721124935000
}
```

#### 🧾 Sample Payment Record

```json
{
  "payment_id": "uuid",
  "order_id": "same_as_order_id",
  "payment_amount": 52.30,
  "payment_method": "credit_card",
  "payment_time": 1721124960000
}
```

---

### 3. 🚀 ksqlDB Stream Processing

#### 🔹 Create Streams

```sql
CREATE STREAM macd_orders_stream (
  order_id STRING,
  ...
) WITH (
  KAFKA_TOPIC = 'macd_orders',
  ...
);
```

```sql
CREATE STREAM macd_payments_stream (
  payment_id STRING,
  ...
) WITH (
  KAFKA_TOPIC = 'macd_payments',
  ...
);
```

#### 🔗 Real-Time Join

```sql
CREATE STREAM macd_orders_payments_joined AS
SELECT ...
FROM macd_orders_stream o
INNER JOIN macd_payments_stream p
  WITHIN 24 HOURS
  ON o.order_id = p.order_id
EMIT CHANGES;
```

This produces a joined stream of orders + matching payments.

---

### 4. 🌐 MongoDB Integration

* Created a **MongoDB Atlas cluster** in `ap-south-1` (to match Kafka region).
* Integrated **ksqlDB Sink Connector** to stream `macd_orders_payments_joined` into MongoDB.
* Target Collection: `orders_payments_joined`

#### 🧠 Why MongoDB?

* Flexible schema for nested `order_items`
* Fast querying for BI dashboards
* Ideal for semi-structured analytical workloads

---

## 📊 Architecture

![Streaming Flow](assets/architecture.png)

---

## 🧹 Next Steps

* Add windowed aggregations (e.g., hourly revenue)
* Visualize in a dashboard (e.g., Grafana / MongoDB Charts)
* Add alerting (e.g., payment mismatches)

---

## 📚 Learnings

* ✅ Kafka Streams via Python (Confluent)
* ✅ Schema evolution with Avro
* ✅ Real-time joins in ksqlDB with `WITHIN 24 HOURS`
* ✅ Region-matching for Confluent ↔ MongoDB connectivity

---

## 📬 Contact

Have questions? Connect with me on [LinkedIn](#) or raise an issue here.

```

---

Let me know if you'd like me to generate the `architecture.png` file content or help you push this project to GitHub with a license, `.gitignore`, etc.
```
