from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

spark = SparkSession.builder \
      .appName("StreamJob") \
      .master("local[*]") \
      .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
      .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
      .getOrCreate()

schema = StructSchema = StructType() \
      .add("event_time", StringType()) \
      .add("machine_id", StringType()) \
      .add("temperature", DoubleType()) \
      .add("vibration", DoubleType()) \
      .add("rpm", IntegerType())

raw = spark.readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "localhost:9092") \
      .option("subscribe", "machine-sensors") \
      .load()

parsed = raw.selectExpr("CAST(value AS STRING) as json") \
      .select(from_json(col("json"), schema).alias("d")) \
      .select("d.*")

query = parsed.writeStream \
      .format("delta") \
      .option("checkpointLocation", "checkpoints/sensors") \
      .option("path", "delta/sensors") \
      .outputMode("append") \
      .start()

query.awaitTermination()