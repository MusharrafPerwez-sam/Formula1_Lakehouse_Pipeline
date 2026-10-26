# Databricks notebook source
# MAGIC %md 
# MAGIC 1. Update Delta Table
# MAGIC 2. Delete From Delta Table

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE f1_demo.results_managed 
# MAGIC SET points = 11 - position

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed

# COMMAND ----------

from delta.tables import *

deltaTable = DeltaTable.forPath(spark, '/mnt/formula1dlmorales/demo/results_managed')

# Declare the predicate by using a SQL-formatted string.
deltaTable.update(
  condition = "position <= 10",
  set = { "points": "11 - position" }
)

# COMMAND ----------

# MAGIC %sql 
# MAGIC DELETE FROM f1_demo.results_managed
# MAGIC WHERE points = 0

# COMMAND ----------

