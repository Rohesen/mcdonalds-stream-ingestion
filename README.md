# 🍔 Real-Time McDonald's Orders & Payments Streaming Pipeline

This project demonstrates how to simulate and stream real-time McDonald's order and payment data using **Apache Kafka**, **ksqlDB**, and **MongoDB Atlas**. It features a fully working data pipeline that supports real-time ingestion, stream joins, and analytical querying — visualized in MongoDB Dashboards.

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

## 📂 Project Structure

```
.
├── kafka_producer.py                # Python script for mock data generation
├── stream_definitions.sql           # ksqlDB stream creation and join logic
├── Project_Screenshots/             # Architecture & setup screenshots
│   ├── mcdonalds-streaming-rohesen.png
│   ├── ss_order_stream.png
│   ├── ss_payment_stream.png
│   ├── ss_code_1.png
│   ├── ss_code_2.png
│   ├── ss_mongodb_cluster.png
│   └── mongodb_dashboard.png
├── README.md                        # Project documentation
```

---

## 🧱 Architecture Overview

![Architecture Diagram](Project_Screenshots/mcdonalds-streaming-rohesen.png)

---

## 🐍 Python Producer

The mock data generator produces:

* 500 **orders**
* 500 **payments**
  Each order and payment pair is matched via a common `order_id`.

📸 Code Snippets:
![Producer Code Part 1](Project_Screenshots/ss_code_1.png)
![Producer Code Part 2](Project_Screenshots/ss_code_2.png)

---

## 🔄 Kafka Topics

Two Avro-serialized topics were created in **Confluent Cloud**:

* `macd_orders`
* `macd_payments`

Each topic uses schemas stored in **Confluent Schema Registry**.

---

## 🔁 Stream Processing via ksqlDB

Streams were defined in **ksqlDB** to process and enrich data:

### ✅ Order Stream

```sql
CREATE STREAM macd_orders_stream (...) WITH (...);
```

📸 Screenshot:
![Order Stream](Project_Screenshots/ss_order_stream.png)

### ✅ Payment Stream

```sql
CREATE STREAM macd_payments_stream (...) WITH (...);
```

📸 Screenshot:
![Payment Stream](Project_Screenshots/ss_payment_stream.png)

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
![MongoDB Cluster](Project_Screenshots/ss_mongodb_cluster.png)

---

## 📈 MongoDB Dashboard

Once data was streamed into MongoDB, **MongoDB Charts** was used to build visualizations — like most popular items, payment methods, or hourly revenue.

📸 Dashboard Screenshot:
![MongoDB Chart](Project_Screenshots/mongodb_dashboard.png)

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
