from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

spark = (
    SparkSession.builder
        .appName("PySparkKafkaApp")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1")
        .getOrCreate()
)

df = (
    spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("subscribe", "input_topic")
            .option("startingOffsets", "earliest")
            .load()
)

df2 = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

df3 = df2.withColumn("processed_value",
                        expr("concat(value, ' at ', current_timestamp())"))

console_query = (
    df3.writeStream
        .format("console")
        .option("truncate", "false")
        .start()
)

kafka_sink = (
    df3.selectExpr("CAST(key AS STRING) AS key",
                    "CAST(processed_value AS STRING) AS value")
        .writeStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("topic", "output_topic")
        .option("checkpointLocation", "/tmp/checkpoints/pykafka_app")
        .start()
)

spark.streams.awaitAnyTermination()
