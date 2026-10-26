-- Databricks notebook source
-- MAGIC %md
-- MAGIC 1. Create external table using Python
-- MAGIC 2. Create external table using SQL
-- MAGIC 3. Effect of dropping an external table
-- MAGIC

-- COMMAND ----------

-- MAGIC %run "../Includes/configuration"

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC race_results_df = spark.read.parquet(f"{presentation_folder_path}/race_results")
-- MAGIC race_results_df.write.format("parquet").option("path", f"{presentation_folder_path}/race_results_ext_py").saveAsTable('demo.race_results_ext_py')

-- COMMAND ----------

SHOW TABLES IN demo

-- COMMAND ----------

DESC EXTENDED demo.race_results_ext_py

-- COMMAND ----------

DROP TABLE IF EXISTS demo.race_results_ext_sql; 

CREATE EXTERNAL TABLE demo.race_results_ext_sql
(
  race_year INT,
  race_name STRING,
  race_date TIMESTAMP,
  circuit_location STRING,
  driver_name STRING,
  driver_number STRING,
  driver_nationality STRING,
  team STRING,
  fastest_lap INT,
  position INT,
  race_time STRING,
  points INT,
  created_date TIMESTAMP
)
USING parquet
LOCATION "/mnt/formula1dlmorales/presentation/race_results_ext_sql"

-- COMMAND ----------

INSERT INTO demo.race_results_ext_sql 
SELECT * FROM demo.race_results_ext_py WHERE race_results_ext_py.race_year = 2020;

-- COMMAND ----------

SELECT count(*) FROM demo.race_results_ext_sql;