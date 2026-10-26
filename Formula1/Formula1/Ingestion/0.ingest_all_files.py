# Databricks notebook source
v_result = dbutils.notebook.run('1.ingest_circuits_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('2.ingest_races_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('3.ingest_constructors_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('4.ingest_drivers_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('5.ingest_results_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('6.ingest_pit_stops_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('7.ingest_laptimes_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

v_result = dbutils.notebook.run('8.ingest_qualifying_files', 0, {"p_file_date":"2021-03-28"})

# COMMAND ----------

v_result

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN f1_processed;
# MAGIC SELECT race_id, COUNT(*) FROM f1_processed.qualifying
# MAGIC GROUP BY race_id

# COMMAND ----------

