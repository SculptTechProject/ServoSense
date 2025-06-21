from fastapi import FastAPI, Response
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel
import os
import csv
from datetime import datetime, timedelta
from kafka import KafkaProducer
import json
import random
import joblib
import pandas as pd
from pathlib import Path
from typing import List
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

SIM_COUNT   = Counter("servo_sim_requests_total", "Number of /simulate calls")
TEMP_GAUGE  = Gauge(  "servo_sim_temperature",   "Last simulated temperature", ["machine_id"])
VIB_GAUGE   = Gauge(  "servo_sim_vibration",     "Last simulated vibration", ["machine_id"])
RPM_GAUGE   = Gauge(  "servo_sim_rpm",           "Last simulated rpm",       ["machine_id"])

current_time = datetime.utcnow()

file_path = "../batch/data/sensors.csv" # Can get data from DB there ;)

CSV_FILE   = Path("/app/data/sensors.csv") # Absolute path in container (docker)  
KAFKA_TOPIC = "machine-sensors"

producer = KafkaProducer(
      bootstrap_servers="kafka:9092",
      value_serializer=lambda v: json.dumps(v).encode()
)


@app.get("/")
def read_root():
      return {"message": "Server is working!"}

# ---------------------------------------------------------

class Sensor(BaseModel):
      event_time: datetime | None = None
      machine_id: str
      temperature: float
      vibration: float
      rpm: int

@app.post("/sensor", response_model=Sensor)
def add_sensor(sensor: Sensor):
      if sensor.event_time is None:
            sensor.event_time = datetime.utcnow()

      rec = sensor.model_dump(mode="python")
      rec["event_time"] = rec["event_time"].isoformat() + "Z"

      CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
      write_header = not CSV_FILE.exists()

      with CSV_FILE.open("a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                  writer.writerow(rec.keys())
            writer.writerow(rec.values())

      producer.send(KAFKA_TOPIC, rec)
      producer.flush()

      return sensor


# GET endpoint to return all stored sensor records
@app.get("/sensor", response_model=List[dict])
def get_sensors():
      if not os.path.exists(file_path):
            return []
      with open(file_path, newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

# ---------------------------------------------------------


@app.get("/simulate", response_model=Sensor)
def simulate():
      global current_time
      delta = timedelta(seconds=random.uniform(0.05, 0.15))
      current_time += delta

      sensor = Sensor(
            event_time  = current_time,
            machine_id  = random.choice(["M-001","M-002","M-003","M-004","M-005"]),
            temperature = round(random.uniform(60, 90), 2),
            vibration   = round(random.uniform(0.0, 0.3), 3),
            rpm         = random.randint(1000, 2500)
      )

      SIM_COUNT.inc()
      TEMP_GAUGE.labels(machine_id=sensor.machine_id).set(sensor.temperature)
      VIB_GAUGE.labels( machine_id=sensor.machine_id).set(sensor.vibration)
      RPM_GAUGE.labels( machine_id=sensor.machine_id).set(sensor.rpm)

      return sensor

# ---------------------------------------------------------

model = joblib.load("../serving/model_rf.pkl")

@app.get("/predict_all", response_model=List[dict])
def predict_all():
      df = pd.read_csv("data/sensors.csv", parse_dates=["event_time"])
      df["hour"]   = df["event_time"].dt.hour
      df["minute"] = df["event_time"].dt.minute
      df["second"] = df["event_time"].dt.second

      features = ["temperature","vibration","rpm","hour","minute","second"]
      X_all = df[features]

      df["is_hot"]    = model.predict(X_all)
      df["probability"] = model.predict_proba(X_all)[:,1]

      return df.to_dict(orient="records")

# ---------------------------------------------------------

@app.get("/metrics")
def metrics():
      data = generate_latest()
      return Response(content=data, media_type=CONTENT_TYPE_LATEST)