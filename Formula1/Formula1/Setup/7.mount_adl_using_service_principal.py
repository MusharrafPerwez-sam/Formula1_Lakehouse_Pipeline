# Databricks notebook source
# MAGIC %md
# MAGIC #### Mount Azure Data Lake using Service Principal
# MAGIC   <ol>
# MAGIC       <li> Get client_id, tenant_id and client_secret from key vault </li>
# MAGIC       <li> Get Spark Config with App/Client id, Directory/ Tenant id & Secret</li>
# MAGIC       <li> Call file system utility mount to mount the storage</li>
# MAGIC       <li> Explore other file system utilities related to mount (list all mounts, unmount)</li>
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

configs = {
    "fs.azure.account.auth.type" : "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": client_id,
    "fs.azure.account.oauth2.client.secret": client_secret,
    "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
}

# COMMAND ----------

dbutils.fs.mount(
    source = "abfss://demo@formula1dlmorales.dfs.core.windows.net/",
    mount_point = "/mnt/formula1dl/demo",
    extra_configs = configs
)

# COMMAND ----------

display(dbutils.fs.ls("/mnt/formula1dl/demo"))

# COMMAND ----------

df = spark.read.csv("/mnt/formula1dl/demo/circuits.csv")
display(df)

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

dbutils.fs.unmount('/mnt/formula1dl/demo')

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

