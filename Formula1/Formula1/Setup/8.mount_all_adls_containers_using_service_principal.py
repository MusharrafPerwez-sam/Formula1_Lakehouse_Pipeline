# Databricks notebook source
# MAGIC %md
# MAGIC #### Mount All Azure Data Lake Container using Service Principal
# MAGIC
# MAGIC

# COMMAND ----------

def mount_adls(container_name, storage_name):
    # Get the credentials usgin Azure Key Vault and Databricks Secret/Scopes
    client_id = dbutils.secrets.get('formula1-scope', 'client-id')
    tenant_id = dbutils.secrets.get('formula1-scope', 'tenant-id')
    client_secret = dbutils.secrets.get('formula1-scope', 'client-secret')

    # Set the configs parameters that is necessary for mounting
    configs = {
    "fs.azure.account.auth.type" : "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": client_id,
    "fs.azure.account.oauth2.client.secret": client_secret,
    "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    }
    mount_destination_path = f"/mnt/{storage_name}/{container_name}"

    # Unmount the container that has the same mount destination
    if any(mount.mountPoint == mount_destination_path for mount in dbutils.fs.mounts()):
        dbutils.fs.unmount(mount_destination_path)
        print(f"Destination mount was unmounted {mount_destination_path}")

    # Mount the different container based on the input
    if (dbutils.fs.mount(
    source = f"abfss://{container_name}@{storage_name}.dfs.core.windows.net/",
    mount_point = mount_destination_path,
    extra_configs = configs 
    )):
        print(f"Mount of '{container_name}' container that belongs to '{storage_name}' storage was mounted successfuly.")
    else:
        print('Something went wrong')


# COMMAND ----------

mount_adls('raw', 'formula1dlmorales')

# COMMAND ----------

mount_adls('processed', 'formula1dlmorales')

# COMMAND ----------

mount_adls('presentation', 'formula1dlmorales')

# COMMAND ----------

mount_adls('demo', 'formula1dlmorales')

# COMMAND ----------

display(dbutils.fs.ls('/mnt/formula1dlmorales/'))

# COMMAND ----------

