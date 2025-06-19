# ServoSense

**ServoSense** is an end-to-end educational project for simulating, ingesting, and analyzing machine sensor data. The pipeline covers:

* Generating synthetic sensor readings (temperature, vibration, RPM) via a REST API
* Storing raw data in CSV files
* Publishing events to Apache Kafka topics
* Running batch analytics with Pandas or Apache Spark
* Processing data streams with Spark Structured Streaming into Delta Lake
* Deploying a simple prediction service and monitoring stack

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
6. [Usage Examples](#usage-examples)
7. [Next Steps](#next-steps)

---

## Features

* **Data Simulation**: FastAPI endpoint (`/sensor`) to generate and retrieve sensor readings, saving them to a CSV file (`data/sensors.csv`).
* **Event Broker**: Kafka topic `machine-sensors` for decoupled communication between services.
* **Batch Processing**: Scripts in `batch/` using Pandas or Spark to compute summary statistics.
* **Stream Processing**: Spark Structured Streaming job in `streaming/` writing to a Delta Lake in `delta/sensors`.
* **Prediction Service**: FastAPI endpoint (`/predict`) in `serving/app.py` for anomaly detection (using scikit-learn and MLflow).
* **Monitoring**: Prometheus and Grafana configurations for metrics collection and dashboarding.

---

## Architecture

```text
[Simulator (FastAPI)] → CSV + Kafka → [Batch Analytics (Pandas/Spark)] → Reports
                               ↘ [Streaming ETL (Spark) → Delta Lake]
                               ↘ [Prediction API (FastAPI)]
                               ↘ [Prometheus → Grafana]
```

---

## Technology Stack

* **Backend & API**: Python, FastAPI, Pydantic
* **Messaging**: Apache Kafka (Bitnami Docker images)
* **Batch Analytics**: Pandas or PySpark
* **Streaming**: Spark Structured Streaming, Delta Lake (`delta-spark`)
* **Machine Learning**: scikit-learn, MLflow
* **Monitoring**: Prometheus, Grafana
* **Orchestration**: Docker Compose

---

## Project Structure

```
servo-sense/
├── simulator/            # FastAPI app for data simulation + CSV + Kafka
│   └── main.py
├── batch/                # Batch ETL scripts (Pandas or Spark)
│   └── batch_job.py
├── streaming/            # Spark Structured Streaming job → Delta Lake
│   └── stream_job.py
├── models/               # Jupyter notebooks and training scripts
│   └── train_model.ipynb
├── serving/              # FastAPI service for predictions
│   └── app.py
├── infra/                # Docker Compose for Zookeeper + Kafka
│   └── docker-compose.yml
├── monitoring/           # Prometheus & Grafana configs
│   └── prometheus.yml
├── data/                 # Raw sensor CSV files
│   └── sensors.csv
├── delta/                # Delta Lake storage for streaming data
├── output/               # Batch output files (CSV/parquet)
└── requirements.txt      # Python dependencies
```

---

## Getting Started

1. **Clone the repository**

   ```bash
   ```

git clone [https://github.com/yourusername/servosense.git](https://github.com/yourusername/servosense.git)
cd servosense

````
2. **Create and activate a virtual environment**
   ```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

3. **Start Kafka infrastructure**

   ```bash
   ```

cd infra
docker-compose up -d
cd ..

````
4. **Run the data simulator API**
   ```bash
cd simulator
uvicorn main:app --reload --port 8000
````

5. **Test adding and retrieving sensor data**

   ```bash
   ```

curl -X POST [http://localhost:8000/sensor](http://localhost:8000/sensor)&#x20;
-H "Content-Type: application/json"&#x20;
-d '{"machine\_id":"M-001","temperature":75.5,"vibration":0.02,"rpm":1500}'

curl [http://localhost:8000/sensor](http://localhost:8000/sensor)

````
6. **Run batch analytics**
   ```bash
cd batch
python batch_job.py
````

7. **Run streaming ETL**

   ```bash
   # soon
   ```

cd streaming
spark-submit --packages io.delta\:delta-core\_2.12:2.4.0 stream\_job.py

```

---

## Usage Examples
- **Data Simulation**: Send POST requests to `/sensor` and observe entries in `data/sensors.csv` and the Kafka topic.
- **Batch Analytics**: Execute `batch_job.py` to see statistics in the console and the `output/hot_readings.csv`.
- **Streaming**: Stream data continuously and inspect the Delta Lake at `delta/sensors`.

---

## Next Steps
- Implement the `/predict` endpoint integrated with a trained ML model.
- Expand batch scripts to write Parquet or Delta format.
- Integrate Prometheus and Grafana for real-time monitoring and alerting.
- Containerize and deploy with Kubernetes or Docker Swarm.

---

**ServoSense** empowers you to learn by building a complete data pipeline from sensor to insight.

```
