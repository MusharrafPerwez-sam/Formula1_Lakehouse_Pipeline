# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest circuits.csv file

# COMMAND ----------

# MAGIC %run "../Includes/configuration"
# MAGIC

# COMMAND ----------

# MAGIC %run  "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text("p_file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("file_date")
display(v_file_date)

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

circuits_schema = StructType(fields=[StructField("circuitId", IntegerType(), False),
                                    StructField("circuitRef", StringType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("location", StringType(), True),
                                    StructField("country", StringType(), True),
                                    StructField("lat", DoubleType(), True),
                                    StructField("lng", DoubleType(), True),
                                    StructField("alt", IntegerType(), True),
                                    StructField("url", StringType(), True)])

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 1: Read our .csv file with our specified schema

# COMMAND ----------

circuits_df = spark.read.options(header=True).schema(circuits_schema).csv(f"{raw_folder_path}/{v_file_date}/circuits.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2: Remove the url column
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col, lit
circuits_selected_df = circuits_df.select(col('circuitId'), col('circuitRef'), col('name'), col('location'), col('country'), col('lat'), col('lng'), col('alt'))

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 3: Rename the columns as required

# COMMAND ----------

circuits_renamed_df = circuits_selected_df.withColumnRenamed('circuitId','circuit_id') \
                                        .withColumnRenamed('circuitRef', 'circuit_ref') \
                                        .withColumnRenamed('lat', 'latitude') \
                                        .withColumnRenamed('lng', 'longitude') \
                                        .withColumnRenamed('alt', 'altitude') \
                                        .withColumn("file_date", lit(v_file_date))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 4: Add ingestion date

# COMMAND ----------

#from pyspark.sql.functions import current_timestamp, lit
#circuits_final_df = circuits_renamed_df.withColumn('ingestion_date', current_timestamp())
circuits_final_df = add_ingestion_date(circuits_renamed_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 5: Write the dataframe as parquet file

# COMMAND ----------

circuits_final_df.write.mode('overwrite').format("delta").saveAsTable("f1_processed.circuits")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_processed.circuits

# COMMAND ----------

dbutils.notebook.exit("Success")