# ServoSense

**ServoSense** is an end-to-end pipeline for processing and analyzing industrial machine sensor data. It consists of several components:

* ​**infra**​: Docker Compose setup for Kafka and Zookeeper
* ​**serving**​: FastAPI application to receive, store, and retrieve sensor readings, plus a simulation endpoint
* ​**simulator**​: Alternative FastAPI service that generates random sensor data every \~0.1 seconds
* ​**streaming**​: PySpark streaming job that reads from Kafka, applies transformations, and writes back to Kafka and console
* ​**batch**​: Python script using Pandas to fetch simulated data every second, append to CSV, and compute basic statistics
* ​**Data\_Analysis**​: Jupyter notebooks for exploratory data analysis (EDA) and Matplotlib visualizations
* ​**models**​: Jupyter notebook for training a predictive maintenance model
* ​**monitoring**​: Prometheus configuration to collect application metrics

---

## Table of Contents

1. [Prerequisites](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#prerequisites)
2. [Installation](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#installation)
3. [Quickstart](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#quickstart)
4. [Project Structure](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#project-structure)
5. [Component Overview](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#component-overview)
6. [Examples](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#examples)
7. [Contact](https://chatgpt.com/c/6855a53f-1fc0-8011-9d08-abaf919fbbee#contact)

---

## Prerequisites

* Python 3.8 or newer
* Docker & Docker Compose
* Java (for Spark, if running streaming)

Install Python dependencies in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Quickstart

### 1. Launch Kafka & Zookeeper

```bash
docker-compose -f infra/docker-compose.yml up -d
```

Verify services:

```bash
docker-compose -f infra/docker-compose.yml ps
```

### 2. Start the FastAPI Server

```bash
cd serving
uvicorn app:app --reload --port 8000
```

Endpoints:

* `POST /sensor` – add a sensor reading
* `GET /sensor` – fetch all stored readings
* `GET /simulate` – generate a single random sensor reading

### 3. Run the Simulator (Optional)

The `simulator` service generates synthetic data every \~0.1s on port 8001.

```bash
cd simulator
uvicorn main:app --reload --port 8001
```

### 4. Streaming with PySpark

```bash
cd streaming
python stream_job.py
```

This job reads from Kafka `input_topic`, appends a timestamp, prints to console, and writes to `output_topic`.

### 5. Batch Processing with Pandas

```bash
cd batch
python batch_job.py
```

This script fetches `/simulate` every second, appends results to `data/sensors.csv`, and prints summary statistics.

### 6. Exploratory Data Analysis (EDA)

Open the notebooks in **Data\_Analysis/** to view histograms, time series plots, and threshold-based visualizations (e.g., points above 80 °C).

### 7. Train Predictive Model

Open **models/train\_model.ipynb** to train and evaluate a predictive maintenance model using scikit-learn.

### 8. Monitoring with Prometheus

Start Prometheus to scrape application metrics:

```bash
prometheus --config.file=monitoring/prometheus.yml
```

---

## Project Structure

```text
ServoSense/
├── infra/                # Docker Compose for Kafka & Zookeeper
│   └── docker-compose.yml
├── serving/              # FastAPI service: ingest, store, simulate readings
│   └── app.py
├── simulator/            # FastAPI simulator generating synthetic data
│   └── main.py
├── streaming/            # PySpark streaming job (stream_job.py)
├── batch/                # batch_job.py + data/sensors.csv
│   ├── batch_job.py
│   └── data/sensors.csv
├── Data_Analysis/        # Jupyter notebooks for EDA and plots
├── models/               # train_model.ipynb for ML training
├── monitoring/           # Prometheus configuration
│   └── prometheus.yml
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## Component Overview

### infra

* Brings up Zookeeper and Kafka in Docker containers.

### serving

* `POST /sensor`: accepts a sensor payload, timestamps it, writes to CSV, and publishes to Kafka topic `machine-sensors`.
* `GET /sensor`: returns all stored readings as JSON.
* `GET /simulate`: returns a single random sensor reading.

### simulator

* Maintains a global `current_time` that increments by a random 0.05–0.15 second delta per request.
* Useful for load testing and continuous data generation on port 8001.

### streaming

* `stream_job.py` sets up a Spark Structured Streaming job:
  * Read from Kafka topic `input_topic`.
  * Transform values and add processing timestamp.
  * Write results to console and Kafka topic `output_topic`.

### batch

* `batch_job.py`: a loop that:
  1. Fetches `/simulate` every second.
  2. Appends each record to `data/sensors.csv`.
  3. Prints simple metrics (e.g., average temperature).

### Data\_Analysis

* Notebooks demonstrating EDA with Pandas and Matplotlib:
  * Histograms of temperature distribution.
  * Time-series plots per machine.
  * Highlight measurements above thresholds.

### models

* `train_model.ipynb`: builds and evaluates a predictive maintenance model using scikit-learn.
* 

### monitoring

* `prometheus.yml`: configures Prometheus to scrape metrics exposed by FastAPI endpoints and client libraries.

---

## Examples

```bash
# Activate environment
source .venv/bin/activate

# Start Kafka & Zookeeper
docker-compose -f infra/docker-compose.yml up -d

# Launch FastAPI server
cd serving && uvicorn app:app --reload

# Run PySpark streaming job
cd streaming
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  stream_job.py
```

---

## Contact

For questions or collaboration, reach out to Mati (project maintainer).

