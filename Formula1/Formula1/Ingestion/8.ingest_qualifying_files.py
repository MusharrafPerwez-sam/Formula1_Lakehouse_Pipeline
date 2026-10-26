# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest qualifying folder where there is a splitted json file into multiple json files
# MAGIC ##### The code consists of defining the schema and reading the csv files, renaming the necessary columns and creating an ingestion_date new one and at last saving the transformed file in parquet format

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text("file_date","2021-03-28")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType
qualifying_schema = StructType(fields = [
    StructField('qualifyId', IntegerType(), False),
    StructField('raceId', IntegerType(), False),
    StructField('driverId', IntegerType(), False),
    StructField('constructorId', IntegerType(), False),
    StructField('number', IntegerType(), False),
    StructField('position', IntegerType(), True),
    StructField('q1', StringType(), False),
    StructField('q2', StringType(), False),
    StructField('q3', StringType(), False),
])

qualifying_df = spark.read.options(header=True, multiline=True).schema(qualifying_schema).json(f'/mnt/formula1dlmorales/raw/{v_file_date}/qualifying')

# COMMAND ----------

display(qualifying_df)

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
qualifying_final_df = qualifying_df.withColumnRenamed('qualifyId', 'qualify_id')\
                               .withColumnRenamed('raceId', 'race_id')\
                               .withColumnRenamed('driverId', 'driver_id')\
                               .withColumnRenamed('constructionId', 'construction_id')\
                               .withColumn('ingestion_date', current_timestamp())\
                               .withColumn('file_date', lit(v_file_date))

# COMMAND ----------

#qualifying_final_df.write.mode('overwrite').format("parquet").saveAsTable("f1_processed.qualifying")
#increment_files(qualifying_final_df, 'race_id', 'f1_processed', 'qualifying')

# COMMAND ----------

final_deduped_df = qualifying_final_df.dropDuplicates(['qualify_id'])

# COMMAND ----------

increment_files_delta(final_deduped_df, 'qualifying.qualify_id = updates.qualify_id AND qualifying.race_id = updates.race_id', 'f1_processed', 'qualifying', '/mnt/formula1dlmorales/processed')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT race_id, count(*) FROM f1_processed.qualifying
# MAGIC GROUP BY race_id

# COMMAND ----------

dbutils.notebook.exit("Success")