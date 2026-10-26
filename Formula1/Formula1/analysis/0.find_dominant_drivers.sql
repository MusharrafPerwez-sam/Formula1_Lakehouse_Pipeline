-- Databricks notebook source
USE f1_presentation

-- COMMAND ----------

SHOW TABLES

-- COMMAND ----------

SELECT driver_name, COUNT(*) AS total_races, SUM(calculated_points) AS total_points, CAST(AVG(calculated_points) AS DECIMAL(3,2)) AS avg_points
FROM calculated_race_results
GROUP BY driver_name
HAVING total_races >= 50
ORDER BY avg_points DESC

-- COMMAND ----------

