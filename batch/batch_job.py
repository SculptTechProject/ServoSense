import pandas as pd

df = pd.read_csv("data/sensors.csv")

print("First 5 rows:\n", df.head())

print("Avg temperature:", df["temperature"].mean())
print("Min vibration:", df["vibration"].min())
print("Max vibration:", df["vibration"].max())
print("Count per machine:\n", df["machine_id"].value_counts())

# Can do this stuff for rpm and vibrations :)
hot = df[df["temperature"] > 85]
hot.to_csv("output/hot_readings.csv", index=False)

print("Hot readings saved to output/hot_readings.csv")