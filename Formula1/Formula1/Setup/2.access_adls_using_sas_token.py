# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using SAS token
# MAGIC   <ol>
# MAGIC       <li> Set the spark config </li>
# MAGIC       <li> List files from demo container </li>
# MAGIC       <li> Read data from circuits.csv file </li>
# MAGIC   </ol>

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

dbutils.secrets.list('formula1-scope')

# COMMAND ----------

sas_token = dbutils.secrets.get('formula1-scope', 'sas-token')

# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type.formula1dlmorales.dfs.core.windows.net", "SAS")
spark.conf.set("fs.azure.sas.token.provider.type.formula1dlmorales.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
spark.conf.set("fs.azure.sas.fixed.token.formula1dlmorales.dfs.core.windows.net", sas_token)

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dlmorales.dfs.core.windows.net/"))

# COMMAND ----------

df = spark.read.csv("abfss://demo@formula1dlmorales.dfs.core.windows.net/circuits.csv")
display(df)