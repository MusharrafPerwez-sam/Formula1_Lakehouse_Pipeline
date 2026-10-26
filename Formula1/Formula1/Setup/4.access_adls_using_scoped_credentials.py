# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using scoped credentials
# MAGIC   <ol>
# MAGIC       <li> Set the spark config fs.azure.account.key in the cluster </li>
# MAGIC       <li> List files from demo container  </li>
# MAGIC       <li> Read data from circuits.csv file </li>
# MAGIC   </ol>

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dlmorales.dfs.core.windows.net/"))

# COMMAND ----------

df = spark.read.csv("abfss://demo@formula1dlmorales.dfs.core.windows.net/circuits.csv")
display(df)