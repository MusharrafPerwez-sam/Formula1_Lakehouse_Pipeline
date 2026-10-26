-- Databricks notebook source
USE f1_presentation

-- COMMAND ----------

-- MAGIC %python
-- MAGIC html = """<h1 style="color:Black;text-align:center;font-family:Ariel">Report on Dominant Fomrula 1 Teams </h1>"""
-- MAGIC displayHTML(html)

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW v_dominant_teams
AS
SELECT team_name, SUM(calculated_points) as total_calculated_points, COUNT(*) AS total_races, AVG(calculated_points) AS avg_score,
      RANK() OVER(ORDER BY AVG(calculated_points) DESC) AS rank
FROM calculated_race_results
GROUP BY team_name
HAVING total_races >= 100
ORDER BY avg_score DESC

-- COMMAND ----------

SELECT race_year, team_name, AVG(calculated_points) as avg_score
FROM calculated_race_results
WHERE team_name IN (SELECT team_name FROM v_dominant_teams WHERE rank < 10)
GROUP BY race_year, team_name

-- COMMAND ----------

SELECT race_year, team_name, COUNT(*) as total_races, AVG(calculated_points) as avg_score
FROM calculated_race_results
WHERE team_name IN (SELECT team_name FROM v_dominant_teams WHERE rank < 10)
GROUP BY race_year, team_name

-- COMMAND ----------

SELECT race_year, team_name, AVG(calculated_points) as avg_score
FROM calculated_race_results
WHERE team_name IN (SELECT team_name FROM v_dominant_teams WHERE rank < 10)
GROUP BY race_year, team_name

-- COMMAND ----------

