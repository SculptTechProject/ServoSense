import joblib
import pandas as pd

model = joblib.load("./model_rf.pkl")

df = pd.read_csv("../batch/data/sensors.csv", parse_dates=["event_time"])

df["hour"]   = df["event_time"].dt.hour
df["minute"] = df["event_time"].dt.minute
df["second"] = df["event_time"].dt.second

features = ["temperature", "vibration", "rpm", "hour", "minute", "second"]
X_all = df[features]

df["is_hot_pred"]    = model.predict(X_all)
df["hot_probability"] = model.predict_proba(X_all)[:,1]

df.to_csv("./output_data/predictions.csv", index=False)
print(df[["event_time","machine_id","temperature","is_hot_pred","hot_probability"]].head())
