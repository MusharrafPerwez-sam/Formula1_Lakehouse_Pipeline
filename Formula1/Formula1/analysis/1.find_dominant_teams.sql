-- Databricks notebook source
USE f1_presentation

-- COMMAND ----------

SHOW TABLES

-- COMMAND ----------



-- COMMAND ----------

SELECT team_name, SUM(calculated_points) as total_calculated_points, COUNT(*) AS total_races, AVG(calculated_points) AS avg_score
FROM calculated_race_results
GROUP BY team_name
HAVING total_races >= 100
ORDER BY score DESC


-- COMMAND ----------

SELECT team_name, SUM(calculated_points) as total_calculated_points, COUNT(*) AS total_races, total_calculated_points / total_races AS score
FROM calculated_race_results
WHERE race_year BETWEEN 2001 AND 2011
GROUP BY team_name
HAVING total_races > 150
ORDER BY score DESC


-- COMMAND ----------

