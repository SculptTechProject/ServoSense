# ServoSense

### Please check pinned project - Servo Sense App on my GitHub account! :)

**ServoSense** is an end-to-end pipeline for processing and analyzing industrial machine sensor data. It integrates data generation, ingestion, streaming, batch processing, EDA, modeling, and monitoring in one cohesive toolkit.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-compose-blue)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🚀 Features

* **Infrastructure**: Docker Compose setup with Kafka, Zookeeper, Prometheus, and Grafana.
* **Serving API**: FastAPI service for sensor data CRUD, simulation, prediction, and health checks.
* **Simulator**: Synthetic data generator (\~10 Hz) with Prometheus metrics.
* **Streaming**: PySpark Structured Streaming for real-time processing.
* **Batch**: Python scripts with Pandas for CSV logging and rolling stats.
* **EDA**: Jupyter notebooks for exploratory analysis and visualization.
* **Models**: Train and serve Random Forest predictive-maintenance models.
* **Monitoring**: Preconfigured Prometheus & Grafana dashboards and alerts.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quickstart](#quickstart)
4. [API Endpoints](#api-endpoints)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## 🛠️ Prerequisites

* Python **3.9** or newer
* Docker & Docker Compose
* Java (for Spark)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ Ensure `scikit-learn` is listed in `requirements.txt` before building Docker images.

---

## ⚙️ Installation

```bash
git clone https://github.com/SculptTechProject/ServoSense.git
cd ServoSense
# Activate environment & install dependencies
```

Build the simulator image:

```bash
docker build -t servo-simulator:latest -f simulator/Dockerfile .
```

Bring up core services:

```bash
docker-compose -f infra/docker-compose.yml up -d
```

---

## 🏃 Quickstart

1. **Start Kafka & Zookeeper**

   ```bash
   ```

docker-compose -f infra/docker-compose.yml up -d kafka zookeeper

````

2. **Run the API Server**

   ```bash
cd serving
uvicorn app:app --reload --port 8000
````

3. **(Optional) Launch Simulator**

   ```bash
   ```

cd simulator
uvicorn main\:app --reload --port 8001

````

4. **Run Streaming Job**

   ```bash
cd streaming
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  stream_job.py
````

5. **Batch Processing**

   ```bash
   ```

cd batch
python batch\_job.py

````

6. **Open EDA Notebooks** in `Data_Analysis/`

7. **Train Model** in `models/train_model.ipynb`

8. **Start Monitoring**

   ```bash
docker-compose -f infra/docker-compose.yml up -d prometheus grafana
````

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000) (admin/admin)

---

## 🔗 API Endpoints

FastAPI serving endpoints:

| Method | Path           | Description                                                                                   |
| ------ | -------------- | --------------------------------------------------------------------------------------------- |
| GET    | `/`            | Health check, returns `{ "message": "Server is working!" }`.                                  |
| POST   | `/sensor`      | Add a new sensor reading (JSON body).                                                         |
| GET    | `/sensor`      | Retrieve all stored sensor readings.                                                          |
| GET    | `/simulate`    | Generate and return a single simulated reading.                                               |
| GET    | `/predict_all` | Run model predictions on all CSV readings, returns list with `is_hot` flag and `probability`. |
| GET    | `/metrics`     | Prometheus metrics endpoint for simulation gauges.                                            |
| GET    | `/health`      | Service health endpoint, returns `{ "status": "ok" }`.                                        |

---

## 📂 Project Structure

```
ServoSense/
├── infra/            # Docker Compose for infra
├── serving/          # FastAPI ingestion & prediction API
├── simulator/        # Synthetic data generator
├── streaming/        # PySpark streaming job
├── batch/            # Batch processing scripts
├── Data_Analysis/    # EDA notebooks
├── models/           # ML training notebook & saved model
├── monitoring/       # Prometheus & Grafana configs
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feat/my-feature`)
5. Open a Pull Request

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

Questions or feedback? Open an issue or ping us on GitHub:

```
github.com/SculptTechProject/ServoSense
```
