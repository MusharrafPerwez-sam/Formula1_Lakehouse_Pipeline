# Databricks notebook source
# MAGIC %sql
# MAGIC USE f1_processed

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text('file_date', '2021-03-28')
v_file_date = dbutils.widgets.get('file_date')

# COMMAND ----------

# MAGIC %sql
# MAGIC --DROP VIEW IF EXISTS race_result_updated

# COMMAND ----------

spark.sql(f"""
        CREATE OR REPLACE TEMP VIEW race_result_updated
        AS
        SELECT ra.race_year, c.name as team_name, d.driver_id, d.name as driver_name, ra.race_id, re.position, re.points, 11 - re.position as calculated_points, re.file_date
        FROM results re
        INNER JOIN races ra ON re.race_id = ra.race_id
        INNER JOIN drivers d ON re.driver_id = d.driver_id
        INNER JOIN constructors c ON c.constructor_id = re.constructor_id
        WHERE re.position <= 10 AND re.file_date = '{v_file_date}'
          """)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS f1_presentation.calculated_race_results
# MAGIC (
# MAGIC   race_year INT,
# MAGIC   team_name STRING,
# MAGIC   driver_id INT,
# MAGIC   driver_name STRING,
# MAGIC   race_id INT,
# MAGIC   position INT,
# MAGIC   points INT,
# MAGIC   calculated_points INT,
# MAGIC   created_date TIMESTAMP,
# MAGIC   updated_date TIMESTAMP
# MAGIC )
# MAGIC USING DELTA

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(1) FROM race_result_updated

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO f1_presentation.calculated_race_results tgt
# MAGIC USING race_result_updated upd
# MAGIC ON (tgt.driver_id = upd.driver_id AND tgt.race_id = upd.race_id)
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     tgt.position = upd.position,
# MAGIC     tgt.points = upd.points,
# MAGIC     tgt.calculated_points = upd.calculated_points,
# MAGIC     tgt.updated_date = current_timestamp
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (
# MAGIC     race_year,
# MAGIC     team_name,
# MAGIC     driver_id,
# MAGIC     driver_name,
# MAGIC     race_id,
# MAGIC     position,
# MAGIC     points,
# MAGIC     calculated_points,
# MAGIC     created_date
# MAGIC   )
# MAGIC   VALUES (
# MAGIC     upd.race_year,
# MAGIC     upd.team_name,
# MAGIC     upd.driver_id,
# MAGIC     upd.driver_name,
# MAGIC     upd.race_id,
# MAGIC     upd.position,
# MAGIC     upd.points,
# MAGIC     upd.calculated_points,
# MAGIC     current_timestamp
# MAGIC   )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(1) FROM f1_presentation.calculated_race_results

# COMMAND ----------

#df_results = spark.table('f1_processed.results')
#df_races = spark.table('f1_processed.races')
#df_drivers = spark.table('f1_processed.drivers')
#df_constructors = spark.table('f1_processed.constructors')

# COMMAND ----------

#from pyspark.sql.functions import lit
#df_final = df_results.join(df_races, df_results.race_id == df_races.race_id, 'inner')\
#                     .join(df_drivers, df_results.driver_id == df_drivers.driver_id, 'inner')\
#                     .join(df_constructors, df_results.constructor_id == df_constructors.constructor_id, 'inner')\
#                     .withColumn('calculated_points', lit(11) - df_results.position)\
#                     .select('race_year', df_constructors.name.alias('team_name'), df_drivers.driver_id, df_drivers.name.alias('driver_name'), df_races.race_id, 'position', 'points', 'calculated_points', )

# COMMAND ----------

##display(df_final)

# COMMAND ----------

