# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest circuits.csv file

# COMMAND ----------

dbutils.widgets.text("file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, DateType

races_schema = StructType(fields=[StructField("raceId", IntegerType(), False),
                                    StructField("year", IntegerType(), True),
                                    StructField("round", IntegerType(), True),
                                    StructField("circuitId", IntegerType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("date", DateType(), True),
                                    StructField("time", StringType(), True),
                                    StructField("url", StringType(), True)])

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 1: Read our .csv file with our specified schema

# COMMAND ----------

races_df = spark.read.options(header=True).schema(races_schema).csv(f"/mnt/formula1dlmorales/raw/{v_file_date}/races.csv")

# COMMAND ----------

display(races_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2: Remove the url column
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col, lit
races_df_filtered = races_df.select(col('raceId'), col('year'), col('round'), col('circuitId'), col('name'), col('date'), col('time'))

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 3: Rename the columns as required

# COMMAND ----------

races_renamed_df = races_df_filtered.withColumnRenamed('raceId', 'race_id') \
                                    .withColumnRenamed('year', 'race_year') \
                                    .withColumnRenamed('round', 'round') \
                                    .withColumnRenamed('circuitId', 'circuit_id')\
                                    .withColumn('file_date', lit(v_file_date))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 4: Combine date and time columns in order to create race_timestamp column and add ingestion date. At last delete date and time columns.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit, to_timestamp, concat

races_final_df = races_renamed_df.withColumn('race_timestamp', to_timestamp(concat(col('date'), lit(' '), col('time')), 'yyyy-MM-dd HH:mm:ss')) \
                                .withColumn('ingestion_date', current_timestamp()) \
                                .drop(col('date'), col('time'))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 5: Write the dataframe as parquet file

# COMMAND ----------

races_final_df.write.mode('overwrite').format("delta").saveAsTable("f1_processed.races")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_processed.races 

# COMMAND ----------

dbutils.notebook.exit("Success")