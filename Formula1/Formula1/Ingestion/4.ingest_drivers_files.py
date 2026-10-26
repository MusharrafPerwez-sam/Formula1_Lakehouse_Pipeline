# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest drivers.json file which have nested columns

# COMMAND ----------

dbutils.widgets.text("file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 1: Define schema and read the .json file using Spark DataFrame reader API

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType

name_schema = StructType(fields = [StructField('forename', StringType(), True),
                                   StructField('surname', StringType(), True)])

drivers_schema = StructType(fields = [StructField('driverId', IntegerType(), False),
                                    StructField('driverRef', StringType(), True),
                                    StructField('number', IntegerType(), True),
                                    StructField('code', StringType(), True),
                                    StructField('name', name_schema, True),
                                    StructField('dob', DateType(), True),
                                    StructField('nationality', StringType(), True),
                                    StructField('url', StringType(), True)])

# COMMAND ----------

drivers_df = spark.read.option('header', True).json(f'/mnt/formula1dlmorales/raw/{v_file_date}/drivers.json')

# COMMAND ----------

display(drivers_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 2: Rename columns and add new columns

# COMMAND ----------

from pyspark.sql.functions import concat, lit, current_timestamp, col
drivers_filtered_df = drivers_df.withColumnRenamed('driverId', 'driver_id')\
                                .withColumnRenamed('driverRef', 'driver_ref')\
                                .withColumn('name', concat(col('name.forename'), lit(' '), drivers_df.name.surname))\
                                .withColumn('ingestion_date', current_timestamp())\
                                .withColumn('file_date', lit(v_file_date))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 3: Drop unwanted coolumns

# COMMAND ----------

drivers_final_df = drivers_filtered_df.drop('url')

# COMMAND ----------

display(drivers_final_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 4: Write the output processed container in parquet format

# COMMAND ----------

drivers_final_df.write.mode('overwrite').format("delta").saveAsTable("f1_processed.drivers")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_processed.drivers

# COMMAND ----------

