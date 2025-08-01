# 🍔 Real-Time McDonald's Orders & Payments Streaming Pipeline

This project demonstrates how to simulate and stream real-time McDonald's order and payment data using **Apache Kafka**, **ksqlDB**, and **MongoDB Atlas**. It features a fully working data pipeline that supports real-time ingestion, stream joins, and analytical querying — visualized in MongoDB Dashboards.

Have a look at demo video of our project👇 

![Project Demo](mcdonalds-streaming-rohesen-project2.gif)
---

## 🛠️ Tech Stack

* **Apache Kafka** (Confluent Cloud)
* **ksqlDB**
* **MongoDB Atlas**
* **Python** (Mock data generation)
* **Avro** (Schema serialization)
* **MongoDB Charts**

---

## 📚 Objective

The goal of this project is to:

* Simulate McDonald’s orders and payments in real-time
* Stream data using Kafka topics
* Join streams using `ksqlDB`
* Store enriched records in **MongoDB Atlas**
* Visualize trends via **MongoDB Dashboards**

---

## 🧱 Architecture Overview

![Architecture Diagram](Project_Screenshots/mcdonalds-streaming-rohesen.jpg)

---

## 🐍 Python Producer

The mock data generator produces:

* 500 **orders**
* 500 **payments**
  Each order and payment pair is matched via a common `order_id`.

📸 Code Snippets:

![Producer Code Part 1](Project_Screenshots/ss%20code%201.png)

![Producer Code Part 2](Project_Screenshots/ss%20code%202.png)

---

## 🔄 Kafka Topics

Two Avro-serialized topics were created in **Confluent Cloud**:

* `macd_orders`
* `macd_payments`

Each topic uses schemas stored in **Confluent Schema Registry**.


---


## 🧬 Kafka Schema Definitions (Avro)

Avro schemas were registered in **Confluent Schema Registry** for the two topics — `macd_orders` and `macd_payments`.

### 🧾 Order Schema

```json
{
  "type": "record",
  "name": "Order",
  "namespace": "com.mcdonalds",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "order_total", "type": "double"},
    {
      "name": "order_items",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "Item",
          "fields": [
            {"name": "item_name", "type": "string"},
            {"name": "quantity", "type": "int"},
            {"name": "price", "type": "double"}
          ]
        }
      }
    },
    {
      "name": "order_time",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
      }
    }
  ]
}
```

### 💳 Payment Schema

```json
{
  "type": "record",
  "name": "Payment",
  "namespace": "com.mcdonalds",
  "fields": [
    {"name": "payment_id", "type": "string"},
    {"name": "order_id", "type": "string"},
    {"name": "payment_amount", "type": "double"},
    {"name": "payment_method", "type": "string"},
    {
      "name": "payment_time",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
      }
    }
  ]
}
```



---

## 🔁 Stream Processing via ksqlDB

Streams were defined in **ksqlDB** to process and enrich data:

### ✅ Order Stream

```sql
CREATE STREAM macd_orders_stream (...) WITH (...);
```

📸 Screenshot:

![Order Stream](Project_Screenshots/ss%20order%20stream.png)


### ✅ Payment Stream

```sql
CREATE STREAM macd_payments_stream (...) WITH (...);
```

📸 Screenshot:

![Payment Stream](Project_Screenshots/ss%20payment_stream.png)

---

### 🔗 Stream Join

A joined stream `macd_orders_payments_joined` was created to correlate orders with their respective payments:

```sql
CREATE STREAM macd_orders_payments_joined AS
SELECT ...
FROM macd_orders_stream o
JOIN macd_payments_stream p
  WITHIN 24 HOURS
  ON o.order_id = p.order_id
EMIT CHANGES;
```

---

## 🧩 MongoDB Integration

MongoDB Atlas was used to store the joined output.

* Region: `ap-south-1` (same as Kafka for minimal latency)
* Collection: `orders_payments_joined`
* Data ingestion via **MongoDB Kafka Sink Connector**

📸 Screenshot of the Cluster:

![MongoDB Cluster](Project_Screenshots/ss%20mongodb_cluster.png)



---

## 📈 MongoDB Dashboard

Once data was streamed into MongoDB, **MongoDB Charts** was used to build visualizations — like most popular items, payment methods, or hourly revenue.

📸 Dashboard Screenshot:

![MongoDB Chart](Project_Screenshots/Screenshot%20mongodb%20dashboard.png)

---

## 📈 Sample Use Cases

* Identify most frequently ordered items
* Monitor peak sales hours
* Compare revenue across payment methods
* Detect payment mismatches

---

## 🚀 Next Steps

* Add time-windowed aggregations (TUMBLING / HOPPING windows)
* Stream to other sinks like **ClickHouse**, **Postgres**, or **ElasticSearch**
* Alerting on anomalies using **Kafka Streams** or **ksqlDB alerts**
* Real-time frontend dashboard with **Streamlit** or **Grafana**

----
