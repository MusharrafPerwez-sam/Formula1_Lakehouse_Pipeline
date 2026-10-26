# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest results.json files as we did before

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text("file_date", "2021-03-28")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 1: Define schema and load the json file using Spark Dataframe reader API

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, LongType, DecimalType
results_schema = StructType(fields = [StructField('resultId', IntegerType(), False),
                                      StructField('raceId', IntegerType(), False),
                                      StructField('driverId', IntegerType(), False),
                                      StructField('constructorId', IntegerType(), False),
                                      StructField('number', IntegerType(), True),
                                      StructField('grid', IntegerType(), True),
                                      StructField('position', IntegerType(), True),
                                      StructField('positionText', StringType(), True),
                                      StructField('positionOrder', IntegerType(), True),
                                      StructField('points', IntegerType(), True),
                                      StructField('laps', IntegerType(), True),
                                      StructField('time', StringType(), True),
                                      StructField('milliseconds', LongType(), True),
                                      StructField('fastestLap', IntegerType(), True),
                                      StructField('rank', IntegerType(), True),
                                      StructField('fastestLapTime', StringType(), True),
                                      StructField('fastestLapSpeed', DecimalType(), True),
                                      StructField('statusId', IntegerType(), True)
])

# COMMAND ----------

results_df = spark.read.option("header", True).schema(results_schema).json(f'/mnt/formula1dlmorales/raw/{v_file_date}/results.json')

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 2: Rename the Camel Case to Snake Case columns and add a new one named ingestion_date

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
filtered_results_df = results_df.withColumnRenamed('resultId', 'result_id')\
                                .withColumnRenamed('raceId', 'race_id')\
                                .withColumnRenamed('driverId', 'driver_id')\
                                .withColumnRenamed('constructorId', 'constructor_id')\
                                .withColumnRenamed('positionText', 'position_text')\
                                .withColumnRenamed('positionOrder', 'position_order')\
                                .withColumnRenamed('fastestLap', 'fastest_lap')\
                                .withColumnRenamed('fastestLapTime', 'fastest_lap_time')\
                                .withColumnRenamed('fastestLapSpeed', 'fastest_lap_speed')\
                                .withColumn('ingestion_date', current_timestamp())\
                                .withColumn('file_date', lit(v_file_date))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 3: Drop the url column 

# COMMAND ----------

final_results_df = filtered_results_df.drop('statusId')

# COMMAND ----------

display(final_results_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 4: Write the result dataframe as parquet file in processed files
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Method 1 (Incremental Load)

# COMMAND ----------

# for race_id in final_results_df.select("race_id").distinct().collect():
#     if (spark._jsparkSession.catalog().tableExists("f1_processed_results")):
#         spark.sql(f"ALTER TABLE f1_processed.results DROP IF EXISTS PARTITION (race_id = {race_id.race_id})")

# COMMAND ----------

# final_results_df.write.mode('append').partitionBy('race_id').format("parquet").saveAsTable("f1_processed.results")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Method 2

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Method Delta

# COMMAND ----------

final_deduped_df = final_results_df.dropDuplicates(['race_id', 'driver_id'])

# COMMAND ----------

increment_files_delta(final_deduped_df, 'results.result_id = updates.result_id AND results.race_id = updates.race_id', 'f1_processed', 'results', '/mnt/formula1dlmorales/processed')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT race_id, COUNT(1)
# MAGIC FROM f1_processed.results
# MAGIC GROUP BY race_id;
# MAGIC
# MAGIC --SELECT COUNT(*) 
# MAGIC --FROM f1_processed.results

# COMMAND ----------

