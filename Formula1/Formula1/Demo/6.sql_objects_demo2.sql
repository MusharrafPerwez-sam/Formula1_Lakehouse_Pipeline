-- Databricks notebook source
-- MAGIC %md
-- MAGIC 1. Create managed table using Python
-- MAGIC 2. Create managed table using SQL
-- MAGIC 3. Effect of dropping a managed table
-- MAGIC 4. Describe table

-- COMMAND ----------

-- MAGIC %run "../Includes/configuration"

-- COMMAND ----------

-- MAGIC %python
-- MAGIC race_results_df = spark.read.parquet(f"{presentation_folder_path}/race_results")

-- COMMAND ----------

-- MAGIC %python
-- MAGIC race_results_df.write.format("parquet").saveAsTable("demo.race_results_python")

-- COMMAND ----------

USE demo;
SHOW TABLES;

-- COMMAND ----------

DESC EXTENDED race_results_python

-- COMMAND ----------

SELECT race_year, team, sum(points) as total_points, sum(CASE WHEN position = 1 THEN 1 ELSE 0 END) as total_wins FROM demo.race_results_python 
WHERE race_year = 2020
GROUP BY race_year, team
ORDER BY  total_wins, total_points DESC 

-- COMMAND ----------

CREATE TABLE race_results_sql 
AS
SELECT * 
FROM demo.race_results_python
WHERE race_year = 2020;

-- COMMAND ----------

DESC EXTENDED race_results_python

-- COMMAND ----------

DROP TABLE demo.race_results_sql

-- COMMAND ----------

SHOW TABLES in demo

-- COMMAND ----------

