# Databricks notebook source
# MAGIC %md
# MAGIC #### Explore DBFS Root
# MAGIC <ol>
# MAGIC   <li> List all the folders in DBFS root </li>
# MAGIC   <li> Interact with DBFS File Browser </li>
# MAGIC   <li> Upload file to DBFS Root </li>
# MAGIC </ol>

# COMMAND ----------

display(dbutils.fs.ls('/'))

# COMMAND ----------

display(dbutils.fs.ls('/FileStore'))

# COMMAND ----------

display(spark.read.csv('/FileStore/circuits.csv'))

# COMMAND ----------

