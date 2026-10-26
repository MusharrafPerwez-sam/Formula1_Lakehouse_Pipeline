# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using Service Principal
# MAGIC   <ol>
# MAGIC       <li> Register Azure AD Application / Service Principal </li>
# MAGIC       <li> Generate a secret/password for the Application  </li>
# MAGIC       <li> Set Spark Config with App/Client id, Directory/Tenant id & Secret </li>
# MAGIC       <li> Assing Role "Storage Blob Data Contributor" to the Data Lake </li>
# MAGIC   </ol>

# COMMAND ----------

dbutils.secrets.listScopes()


# COMMAND ----------

dbutils.secrets.list('formula1-scope')

# COMMAND ----------

client_id = dbutils.secrets.get('formula1-scope', 'client-id')
tenant_id = dbutils.secrets.get('formula1-scope', 'tenant-id')
client_secret = dbutils.secrets.get('formula1-scope', 'client-secret')

# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type.formula1dlmorales.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.formula1dlmorales.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.formula1dlmorales.dfs.core.windows.net", client_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.formula1dlmorales.dfs.core.windows.net", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.formula1dlmorales.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dlmorales.dfs.core.windows.net/"))

# COMMAND ----------

df = spark.read.csv("abfss://demo@formula1dlmorales.dfs.core.windows.net/circuits.csv")
display(df)

# COMMAND ----------

