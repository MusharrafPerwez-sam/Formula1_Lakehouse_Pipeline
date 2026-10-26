# Databricks notebook source
# MAGIC %run "../Includes/configuration"

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text('file_date', '2021-03-28')
v_file_date = dbutils.widgets.get('file_date')

# COMMAND ----------

df_circuits = spark.read.format("delta").load(f"{processed_folder_path}/circuits").withColumnRenamed('location', 'circuit_location')
df_drivers = spark.read.format("delta").load(f"{processed_folder_path}/drivers").withColumnRenamed('name', 'driver_name')\
                                                                   .withColumnRenamed('number', 'driver_number')\
                                                                   .withColumnRenamed('nationality', 'driver_nationality')
df_races = spark.read.format("delta").load(f"{processed_folder_path}/races").withColumnRenamed('name', 'race_name')\
                                                               .withColumnRenamed('race_timestamp', 'race_date')
df_constructors = spark.read.format("delta").load(f"{processed_folder_path}/constructors").withColumnRenamed('name', 'team')
df_results = spark.read.format("delta").load(f"{processed_folder_path}/results").withColumnRenamed('time', 'race_time')\
                        .filter(f"file_date = '{v_file_date}'")\
                        .withColumnRenamed("file_date", "result_file_date")

# COMMAND ----------

display(df_results)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Define the filters manually in order to make the join faster

# COMMAND ----------

wanted_year = 0
wanted_location = ''

# COMMAND ----------

# Define the wanted year
if wanted_year and wanted_location:
    df_races = df_races.filter((df_races.race_year == wanted_year) & (df_races.race_name == wanted_location))

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
df_combined = df_races.join(df_circuits, df_races.circuit_id == df_circuits.circuit_id)\
                           .join(df_results, df_races.race_id == df_results.race_id)\
                           .join(df_drivers, df_results.driver_id == df_drivers.driver_id)\
                           .join(df_constructors, df_results.constructor_id == df_constructors.constructor_id)\
                           .select(df_races.race_year, df_races.race_name, df_races.race_date, df_circuits.circuit_location, df_drivers.driver_name,\
                               df_drivers.driver_number, df_drivers.driver_nationality, df_constructors.team, df_results.fastest_lap, df_results.position, df_results.race_time,\
                               df_results.points, df_results.result_file_date, df_races.race_id)\
                           .withColumn('created_date', current_timestamp())\
                           .withColumnRenamed('result_file_date', 'file_date')

# COMMAND ----------

from pyspark.sql.functions import desc, asc
display(df_combined.orderBy(df_combined.points.desc()))

# COMMAND ----------

#df_combined.write.mode('overwrite').format("parquet").saveAsTable("f1_presentation.race_results")

# COMMAND ----------

#increment_files(df_combined, "race_id", "f1_presentation", "race_results")

# COMMAND ----------

increment_files_delta(df_combined, 'race_results.race_id = updates.race_id AND race_results.driver_name = updates.driver_name', 'f1_presentation', 'race_results', '/mnt/formula1dlmorales/presentation')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT race_id, COUNT(*) FROM f1_presentation.race_results
# MAGIC GROUP BY race_id

# COMMAND ----------

