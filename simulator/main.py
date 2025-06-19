from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel
import os
import csv
from datetime import datetime
from kafka import KafkaProducer
import json

app = FastAPI()

file_path = "data/sensors.csv" # Can get data from DB there ;)

producer = KafkaProducer(
      bootstrap_servers="localhost:9092",
      value_serializer=lambda v: json.dumps(v).encode()
)

@app.get("/")
def read_root():
      return {"message": "Server is working!"}

# ---------------------------------------------------------

class Sensor(BaseModel):
      machine_id: str
      temperature: float
      vibration: float
      rpm: int

@app.post("/sensor")
def add_sensor(sensor: Sensor):
      # prepare record with timestamp
      record = sensor.dict()
      record["event_time"] = datetime.utcnow().isoformat() + "Z"

      # ensure data directory exists
      os.makedirs(os.path.dirname(file_path), exist_ok=True)
      file_exists = os.path.exists(file_path)

      # append to CSV
      with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
      if not file_exists:
            writer.writerow(["event_time", "machine_id", "temperature", "vibration", "rpm"])
      writer.writerow([
            record["event_time"],
            record["machine_id"],
            record["temperature"],
            record["vibration"],
            record["rpm"]
      ])

      producer.send("machine-sensors", record)
      producer.flush()

      return record


# GET endpoint to return all stored sensor records
@app.get("/sensor", response_model=List[dict])
def get_sensors():
      # Return all records from CSV
      if not os.path.exists(file_path):
            return []
      with open(file_path, newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)