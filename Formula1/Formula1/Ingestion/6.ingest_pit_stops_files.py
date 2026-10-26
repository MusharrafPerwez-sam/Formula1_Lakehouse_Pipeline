# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest pit_stop json files

# COMMAND ----------

dbutils.widgets.text("file_date", "2021-03-28")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 1: Define the schema and load the json file

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

pit_stops_schema = StructType(fields=[StructField("raceId", IntegerType(), False),
                                     StructField("driverId", IntegerType(), False),
                                     StructField("stop", IntegerType(), False),
                                     StructField("lap", IntegerType(), False),
                                     StructField("time", StringType(), False),
                                     StructField("duration", StringType(), False),
                                     StructField("milliseconds", IntegerType(), False),
])

pit_stops_df = spark.read.options(multiline=True).schema(pit_stops_schema).json(f'/mnt/formula1dlmorales/raw/{v_file_date}/pit_stops.json')

# COMMAND ----------

display(pit_stops_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 2: Transform from Camel Case to Snake Case and add ingestion_date column

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
pit_stops_filtered_df = pit_stops_df.withColumnRenamed('raceId', 'race_id')\
                                    .withColumnRenamed('driverId','driver_id')\
                                    .withColumn('ingestion_date', current_timestamp())\
                                    .withColumn('file_date', lit(v_file_date))

# COMMAND ----------

#increment_files(pit_stops_filtered_df, 'race_id', 'f1_processed', 'pit_stops')

# COMMAND ----------

final_deduped_df = pit_stops_filtered_df.dropDuplicates(['race_id', 'driver_id', 'stop'])

# COMMAND ----------

increment_files_delta(final_deduped_df, 'pit_stops.race_id = updates.race_id AND pit_stops.driver_id = updates.driver_id AND pit_stops.stop = updates.stop', 'f1_processed', 'pit_stops', '/mnt/formula1dlmorales/processed')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT race_id, COUNT(race_id) FROM f1_processed.pit_stops GROUP BY race_id

# COMMAND ----------

dbutils.notebook.exit("Success")