# ServoSense

**ServoSense** is an end‑to‑end pipeline for processing and analyzing industrial machine sensor data. It consists of several components:

- **infra** – Docker Compose setup for Kafka, Zookeeper, Prometheus and optional Grafana
- **serving** – FastAPI application that receives, stores and retrieves sensor readings (includes a single‑shot simulation endpoint)
- **simulator** – Stand‑alone FastAPI service that continuously generates synthetic sensor data (\~0.1 s interval) on port **8001**
- **streaming** – PySpark Structured Streaming job that reads from Kafka, transforms data and writes back to Kafka / console
- **batch** – Python script that fetches simulated data every second, appends to CSV and computes basic statistics
- **Data_Analysis** – Jupyter notebooks for exploratory data analysis (EDA) and Matplotlib visualisations
- **models** – Notebook for training a predictive‑maintenance model with scikit‑learn
- **monitoring** – Prometheus (and optional Grafana) configuration

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quickstart](#quickstart)
4. [Project Structure](#project-structure)
5. [Component Overview](#component-overview)
6. [Examples](#examples)
7. [Contact](#contact)

---

## Prerequisites

- Python **3.8+**
- Docker & Docker Compose
- Java (required by Spark)

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate        # PowerShell: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

> **Heads‑up:** `scikit-learn` is used by the simulator and model notebook—make sure it is listed in *requirements.txt* before building Docker images.

---

## Installation

```bash
# Clone the repo
git clone https://github.com/SculptTechProject/ServoSense.git
cd ServoSense

# Activate your virtual env & install deps (see above)
```

Build the simulator image (includes **scikit-learn**):

```bash
docker build -t servo-simulator:latest -f simulator/Dockerfile .
```

Bring up the infrastructure:

```bash
docker compose -f infra/docker-compose.yml up -d
```

---

## Quickstart

### 1. Start Kafka & Zookeeper

```bash
docker compose -f infra/docker-compose.yml up -d kafka zookeeper
docker compose -f infra/docker-compose.yml ps
```

### 2. Run the FastAPI server

```bash
cd serving
uvicorn app:app --reload --port 8000
```

Key endpoints:


| Method | Path      | Purpose                      |
| ------ | --------- | ---------------------------- |
| POST   | /sensor   | Store a sensor reading       |
| GET    | /sensor   | Retrieve all stored readings |
| GET    | /simulate | Generate 500 random reading  |

### 3. (Optional) Run the Simulator

```bash
cd simulator
uvicorn main:app --reload --port 8001
```

The simulator emits new data every \~0.1 s and exposes Prometheus metrics at `/metrics`.

### 4. Streaming with PySpark

```bash
cd streaming
python stream_job.py
```

The job reads from topic **machine-sensors**, enriches each event with a processing timestamp and writes the result to **machine-sensors-processed** as well as the console.

### 5. Batch Processing with Pandas

```bash
cd batch
python batch_job.py
```

The script queries the simulator every second, appends rows to `data/sensors.csv` and prints rolling statistics.

### 6. Exploratory Data Analysis

Open the notebooks in **Data\_Analysis/** to explore histograms, time‑series plots and threshold-based visualisations.

### 7. Train the Predictive Model

Open **models/train\_model.ipynb** and follow the notebook to train and evaluate a random‑forest classifier for predictive maintenance.

### 8. Monitoring

Start Prometheus (and optionally Grafana):

```bash
docker compose -f infra/docker-compose.yml up -d prometheus grafana
```

Visit:

- Prometheus – [http://localhost:9090](http://localhost:9090)
- Grafana – [http://localhost:3000](http://localhost:3000) (default credentials: *admin / admin*)

The default `monitoring/prometheus.yml` scrapes:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs: [{ targets: ['localhost:9090'] }]
  - job_name: servo-simulator
    static_configs: [{ targets: ['servo-simulator:8001'] }]
```

---

## Project Structure

```text
ServoSense/
├── infra/                # Docker Compose files
├── serving/              # FastAPI ingest API
├── simulator/            # Continuous data generator
├── streaming/            # PySpark Structured Streaming job
├── batch/                # Batch fetch + stats
├── Data_Analysis/        # Jupyter notebooks (EDA)
├── models/               # ML training notebook
├── monitoring/           # Prometheus / Grafana config
├── requirements.txt
└── README.md
```

---

## Component Overview

- Zookeeper and Kafka containers (plus Prometheus & Grafana)

* Timestamps and stores sensor payloads
* Publishes events to Kafka topic **machine-sensors**

- Generates synthetic sensor events at \~10 Hz
- Loads pre‑trained model `model_rf.pkl`
- Exposes `/metrics` for Prometheus

* Structured Streaming job that:
  - Reads from **machine-sensors**
  - Adds processing timestamp
  - Writes to console and **machine-sensors-processed**

- Polls `/simulate` once per second
- Appends rows to CSV and prints summary stats

---

## Examples

```bash
# Activate env
source .venv/bin/activate

# Infra
docker compose -f infra/docker-compose.yml up -d

# API
cd serving && uvicorn app:app --reload

# Streaming
cd streaming
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  stream_job.py
```

---

## Contact

Questions? Open an issue or ping **@sculpttechproject** 😊
