-- Databricks notebook source
USE f1_processed;

-- COMMAND ----------

SHOW TABLES

-- COMMAND ----------

SELECT * FROM drivers

-- COMMAND ----------

SELECT SPLIT(name, ' ')[0] AS name
FROM drivers

-- COMMAND ----------

SELECT nationality, COUNT(*) as num_of_people
FROM drivers
GROUP BY nationality
ORDER BY num_of_people DESC

-- COMMAND ----------

SELECT nationality, name, dob, RANK() OVER(PARTITION BY nationality ORDER BY dob DESC) as age_rank
FROM drivers
ORDER BY nationality, age_rank

-- COMMAND ----------

