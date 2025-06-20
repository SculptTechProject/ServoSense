# ServoSense

**ServoSense** is an end-to-end pipeline for processing and analyzing industrial machine sensor data. It consists of several components:

* ​**infra**​: Docker Compose setup for Kafka and Zookeeper
* ​**serving**​: FastAPI application to receive, store, and retrieve sensor readings, plus a simulation endpoint
* ​**simulator**​: Alternative FastAPI service that generates random sensor data every \~0.1 seconds
* ​**streaming**​: PySpark streaming job that reads from Kafka, applies transformations, and writes back to Kafka and console
* ​**batch**​: Python script using Pandas to fetch simulated data every second, append to CSV, and compute basic statistics
* ​**Data\_Analysis**​: Jupyter notebooks for exploratory data analysis (EDA) and Matplotlib visualizations
* ​**models**​: Jupyter notebook for training a predictive maintenance model using scikit-learn
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

> **Note:** We’ve added **scikit-learn** as a dependency for model training. Make sure `scikit-learn` is present in `requirements.txt` before rebuilding.

---

## Installation

1. Clone the repo:
   ```bash
   
   ```

git clone [https://github.com/yourusername/ServoSense.git](https://github.com/yourusername/ServoSense.git)
cd ServoSense

```
2. Activate your virtual environment and install Python packages as above.
3. Build and tag Docker images (to include scikit-learn in the simulator image):

   ```bash
docker build -t infra-servo-simulator:latest -f simulator/Dockerfile ..
```

4. Launch infrastructure:
   ```bash
   
   ```

docker-compose -f infra/docker-compose.yml up -d

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

The `simulator` service generates synthetic data every \~0.1 s on port 8001. It now requires **scikit-learn** in its Docker context for loading the trained model.

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

This script fetches `/simulate` every second, appends each record to `data/sensors.csv`, and prints summary statistics.

### 6. Exploratory Data Analysis (EDA)

Open the notebooks in **Data\_Analysis/** to view histograms, time series plots, and threshold-based visualizations (e.g., points above 80 °C).

### 7. Train Predictive Model

Open **models/train\_model.ipynb** to train and evaluate a predictive maintenance model using ​**scikit-learn**​.

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
├── simulator/            # FastAPI simulator generating synthetic data (requires sklearn)
│   └── main.py
├── streaming/            # PySpark streaming job (stream_job.py)
├── batch/                # batch_job.py + data/sensors.csv
│   ├── batch_job.py
│   └── data/sensors.csv
├── Data_Analysis/        # Jupyter notebooks for EDA and plots
├── models/               # train_model.ipynb for ML training (scikit-learn)
├── monitoring/           # Prometheus configuration
│   └── prometheus.yml
├── requirements.txt      # Python dependencies (including scikit-learn)
└── README.md             # This file
```

---

## Component Overview

### infra

* Brings up Zookeeper and Kafka in Docker containers.

### serving

* `POST /sensor`: timestamps and stores payload, writes to CSV, publishes to Kafka topic `machine-sensors`.
* `GET /sensor`: returns all stored readings as JSON.
* `GET /simulate`: returns a single random sensor reading.

### simulator

* Maintains a global `current_time` that increments by a random 0.05–0.15 s per request.
* Loads a pre-trained `model_rf.pkl` via joblib (requires scikit-learn).

### streaming

* `stream_job.py` sets up a Spark Structured Streaming job:
  * Read from Kafka topic `input_topic`.
  * Transform values and add processing timestamp.
  * Write results to console and Kafka topic `output_topic`.

### batch

* `batch_job.py`: loop that fetches `/simulate` every second, appends to `data/sensors.csv`, and prints simple metrics.

### Data\_Analysis

* Notebooks demonstrating EDA with Pandas and Matplotlib:
  * Histograms of temperature distribution.
  * Time-series plots per machine.
  * Highlight measurements above thresholds.

### models

* `train_model.ipynb`: builds and evaluates a predictive maintenance model using scikit-learn.

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

For questions or collaboration, reach out to @sculpttechproject

