# Databricks notebook source
# MAGIC %md
# MAGIC #### Create temporary views on dataframes and access them via SQL and Python

# COMMAND ----------

# MAGIC %run "../Includes/configuration"

# COMMAND ----------

race_results_df = spark.read.parquet(f"{presentation_folder_path}/race_results")

# COMMAND ----------

race_results_df.createOrReplaceTempView("v_race_results")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM v_race_results
# MAGIC WHERE race_year = 2020

# COMMAND ----------

race_results_2019_df = spark.sql("SELECT * FROM v_race_results WHERE race_year=2019")

# COMMAND ----------

display(race_results_2019_df)

# COMMAND ----------

