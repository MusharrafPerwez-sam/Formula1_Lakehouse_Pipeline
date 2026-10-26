-- Databricks notebook source
USE f1_presentation

-- COMMAND ----------

-- MAGIC %python
-- MAGIC html = """<h1 style="color:Black;text-align:center;font-family:Ariel">Report on Dominant Formula 1 Drivers </h1>"""
-- MAGIC displayHTML(html)

-- COMMAND ----------

SELECT driver_name,
       COUNT(*) AS total_races,
       SUM(calculated_points) AS total_points,
       CAST(AVG(calculated_points) AS DECIMAL(3,2)) AS avg_points,
       RANK() OVER(ORDER BY AVG(calculated_points) DESC) AS rank
FROM calculated_race_results
GROUP BY driver_name
HAVING total_races >= 50
ORDER BY avg_points DESC

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW v_dominant_drivers
AS
SELECT driver_name,
       COUNT(*) AS total_races,
       SUM(calculated_points) AS total_points,
       CAST(AVG(calculated_points) AS DECIMAL(3,2)) AS avg_points,
       RANK() OVER(ORDER BY AVG(calculated_points) DESC) AS rank
FROM calculated_race_results
GROUP BY driver_name
HAVING total_races >= 50
ORDER BY avg_points DESC

-- COMMAND ----------

SELECT race_year,
       driver_name,
       COUNT(*) AS total_races,
       SUM(calculated_points) AS total_points,
       CAST(AVG(calculated_points) AS DECIMAL(3,2)) AS avg_points
FROM calculated_race_results
WHERE driver_name IN (SELECT driver_name FROM v_dominant_drivers WHERE rank <= 10)
GROUP BY race_year, driver_name
ORDER BY race_year, avg_points DESC

-- COMMAND ----------

SELECT race_year,
       driver_name,
       COUNT(*) AS total_races,
       SUM(calculated_points) AS total_points,
       CAST(AVG(calculated_points) AS DECIMAL(3,2)) AS avg_points
FROM calculated_race_results
WHERE driver_name IN (SELECT driver_name FROM v_dominant_drivers WHERE rank <= 10)
GROUP BY race_year, driver_name
ORDER BY race_year, avg_points DESC

-- COMMAND ----------

SELECT race_year,
       driver_name,
       COUNT(*) AS total_races,
       SUM(calculated_points) AS total_points,
       CAST(AVG(calculated_points) AS DECIMAL(3,2)) AS avg_points
FROM calculated_race_results
WHERE driver_name IN (SELECT driver_name FROM v_dominant_drivers WHERE rank <= 10)
GROUP BY race_year, driver_name
ORDER BY race_year, avg_points DESC

-- COMMAND ----------

