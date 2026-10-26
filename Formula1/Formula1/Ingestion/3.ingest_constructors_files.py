# Databricks notebook source
# MAGIC %md
# MAGIC ### Read constructors.json file which has JSON format. 

# COMMAND ----------

dbutils.widgets.text("file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2: Define the schema using DDL and read the JSON file using spark dataframe

# COMMAND ----------

constructors_df = spark.read \
                        .schema('constructorId INT, constructorRef STRING, name STRING, nationality STRING, url STRING') \
                        .json(f'/mnt/formula1dlmorales/raw/{v_file_date}/constructors.json')

# COMMAND ----------

display(constructors_df)
constructors_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 3: Rename columns to snake type from camel type, drop the url column and add a new column name ingestion_date

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
constructors_df_final = constructors_df.withColumnRenamed('constructorId', 'constructor_id')\
                                       .withColumnRenamed('constructorRef', 'constructor_ref')\
                                       .drop('url')\
                                       .withColumn('ingestion_date', current_timestamp())\
                                       .withColumn('file_date', lit(v_file_date))

# COMMAND ----------

constructors_df_final.write.mode('overwrite').format("delta").saveAsTable("f1_processed.constructors")

# COMMAND ----------

dbutils.notebook.exit('Success')