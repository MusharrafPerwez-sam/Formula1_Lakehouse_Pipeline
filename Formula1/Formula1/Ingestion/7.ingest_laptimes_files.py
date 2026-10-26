# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest laptimes folder where there is a splitted csv files into multiple csv files
# MAGIC ##### The code consists of defining the schema and reading the csv files, renaming the necessary columns and creating an ingestion_date new one and at last saving the transformed file in parquet format

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text("file_date","2021-03-21")
v_file_data = dbutils.widgets.get("file_date")

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType
laptimes_schema = StructType(fields = [
    StructField('raceId', IntegerType(), False),
    StructField('driverId', IntegerType(), False),
    StructField('lap', IntegerType(), False),
    StructField('position', IntegerType(), True),
    StructField('time', StringType(), True),
    StructField('milliseconds', IntegerType(), True),
])

laptimes_df = spark.read.options(header=True, recursiveFileLookup=True).schema(laptimes_schema).csv(f'/mnt/formula1dlmorales/raw/{v_file_data}/lap_times')

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
laptimes_final_df = laptimes_df.withColumnRenamed('raceId', 'race_id')\
                               .withColumnRenamed('driverId', 'driver_id')\
                               .withColumn('ingestion_date', current_timestamp())\
                               .withColumn('file_date', lit(v_file_data))

# COMMAND ----------

#laptimes_final_df.write.mode('overwrite').format("parquet").saveAsTable("f1_processed.laptimes")

# COMMAND ----------

#increment_files(laptimes_final_df, 'race_id', 'f1_processed', 'lap_times')

# COMMAND ----------

final_deduped_df = laptimes_final_df.dropDuplicates(['race_id', 'driver_id', 'lap'])

# COMMAND ----------

increment_files_delta(final_deduped_df, 'lap_times.race_id = updates.race_id AND lap_times.driver_id = updates.driver_id AND lap_times.lap = updates.lap', 'f1_processed', 'lap_times', '/mnt/formula1dlmorales/processed')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT race_id, COUNT(*) FROM f1_processed.lap_times
# MAGIC GROUP BY race_id;
# MAGIC
# MAGIC SELECT *
# MAGIC from f1_processed.lap_times
# MAGIC WHERE race_id = 1052 AND driver_id = 817

# COMMAND ----------

