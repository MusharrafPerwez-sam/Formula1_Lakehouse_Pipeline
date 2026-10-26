-- Databricks notebook source
-- MAGIC %md
-- MAGIC 1. Create Temp Veiw
-- MAGIC 2. Create Global Temp View
-- MAGIC 3. Create Permanent View

-- COMMAND ----------

-- MAGIC %run "../Includes/configuration"

-- COMMAND ----------

SHOW TABLES FROM demo

-- COMMAND ----------

CREATE OR REPLACE GLOBAL TEMP VIEW v_race_results
AS 
SELECT * FROM demo.race_results_python WHERE race_year = 2018;

-- COMMAND ----------

CREATE OR REPLACE GLOBAL TEMP VIEW gv_race_results
AS 
SELECT * FROM demo.race_results_python WHERE race_year = 2012;

-- COMMAND ----------

CREATE OR REPLACE VIEW demo.pv_race_results
AS 
SELECT * FROM demo.race_results_python WHERE race_year = 2000;

-- COMMAND ----------

SELECT COUNT(*) FROM v_race_results

-- COMMAND ----------

SELECT COUNT(*) FROM global_temp.gv_race_results

-- COMMAND ----------

SHOW TABLES IN demo

-- COMMAND ----------

SELECT COUNT(*) FROM demo.pv_race_results