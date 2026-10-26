# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using access keys
# MAGIC   <ol>
# MAGIC       <li> Set the spark config </li>
# MAGIC       <li> List files from demo container </li>
# MAGIC       <li> Read data from circuits.csv file </li>
# MAGIC   </ol>

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

access_key = dbutils.secrets.get('formula1-scope', 'access-key')

# COMMAND ----------

spark.conf.set(
    "fs.azure.account.key.formula1dlmorales.dfs.core.windows.net",
    access_key
)

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dlmorales.dfs.core.windows.net"))

# COMMAND ----------

df = spark.read.csv("abfss://demo@formula1dlmorales.dfs.core.windows.net/circuits.csv")
display(df)

# COMMAND ----------

