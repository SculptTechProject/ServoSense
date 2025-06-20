import time
import requests
import pandas as pd

max_sen = 500
curr_sen = 1

pd.DataFrame(columns=["event_time","machine_id","temperature","vibration","rpm"]) \
      .to_csv("data/sensors.csv", index=False)

while max_sen > curr_sen:
      resp = requests.get("http://127.0.0.1:8000/simulate")
      record = resp.json()
      pd.DataFrame([record]) \
            .to_csv("data/sensors.csv", mode="a", header=False, index=False)

      curr_sen += 1
      time.sleep(0.01)





