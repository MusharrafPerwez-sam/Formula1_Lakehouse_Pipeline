# Databricks notebook source
# MAGIC %md
# MAGIC Upsert using merge

# COMMAND ----------

drivers_day1_df = spark.read \
    .option("inferSchema", True) \
        .json("/mnt/formula1dlmorales/raw/2021-03-21/drivers.json") \
            .filter("driverId <= 10") \
                .select("driverId", "dob", "name.forename", "name.surname")

# COMMAND ----------

drivers_day1_df.createOrReplaceTempView('drivers_day1')

# COMMAND ----------

display(drivers_day1_df)

# COMMAND ----------

from pyspark.sql.functions import upper
drivers_day2_df = spark.read \
    .option("inferSchema", True) \
        .json("/mnt/formula1dlmorales/raw/2021-03-21/drivers.json") \
            .filter("driverId BETWEEN 6 AND 15") \
                .select("driverId", "dob", upper("name.forename").alias("forename"), upper("name.surname").alias("surname"))

# COMMAND ----------

drivers_day2_df.createOrReplaceTempView('drivers_day2')

# COMMAND ----------

display(drivers_day2_df)

# COMMAND ----------

drivers_day3_df = spark.read \
    .option("inferSchema", True) \
        .json("/mnt/formula1dlmorales/raw/2021-03-21/drivers.json") \
            .filter("driverId BETWEEN 1 AND 5 OR driverId BETWEEN 16 AND 20") \
                .select("driverId", "dob", upper("name.forename").alias("forename"), upper("name.surname").alias("surname"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS f1_demo.drivers_merge (
# MAGIC   driverId INT,
# MAGIC   dob DATE,
# MAGIC   forename STRING,
# MAGIC   surname STRING,
# MAGIC   createDate DATE, 
# MAGIC   updateDate DATE
# MAGIC ) 
# MAGIC USING DELTA

# COMMAND ----------

# MAGIC %md
# MAGIC Day1

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO f1_demo.drivers_merge
# MAGIC USING drivers_day1
# MAGIC ON f1_demo.drivers_merge.driverId = drivers_day1.driverId
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     dob = drivers_day1.dob,
# MAGIC     forename = drivers_day1.forename,
# MAGIC     surname = drivers_day1.surname,
# MAGIC     updateDate = current_timestamp
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (
# MAGIC     driverId,
# MAGIC     dob,
# MAGIC     forename,
# MAGIC     surname,
# MAGIC     createDate
# MAGIC   )
# MAGIC   VALUES (
# MAGIC     drivers_day1.driverId,
# MAGIC     drivers_day1.dob,
# MAGIC     drivers_day1.forename,
# MAGIC     drivers_day1.surname,
# MAGIC     current_timestamp
# MAGIC   )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.drivers_merge

# COMMAND ----------

# MAGIC %md Day2

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.drivers_merge

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO f1_demo.drivers_merge dm
# MAGIC USING drivers_day2 d2
# MAGIC ON dm.driverId = d2.driverId
# MAGIC WHEN MATCHED THEN
# MAGIC UPDATE SET dm.dob = d2.dob,
# MAGIC            dm.forename = d2.forename,
# MAGIC            dm.surname = d2.surname,
# MAGIC            dm.updateDate = current_timestamp
# MAGIC WHEN NOT MATCHED
# MAGIC THEN INSERT (driverId, dob, forename, surname, createDate) VALUES (d2.driverId, d2.dob, d2.forename, d2.surname, current_timestamp)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.drivers_merge

# COMMAND ----------

# MAGIC %md Day3

# COMMAND ----------

from delta.tables import *
from pyspark.sql.functions import current_timestamp
deltaTablePeople = DeltaTable.forPath(spark, '/mnt/formula1dlmorales/demo/drivers_merge')

deltaTablePeople.alias('tgt') \
  .merge(
    drivers_day3_df.alias('d3'),
    'tgt.driverId = d3.driverId'
  ) \
  .whenMatchedUpdate(set =
    {
      "dob": "d3.dob",
      "forename": "d3.forename",
      "surname": "d3.surname",
      "updateDate": current_timestamp(),
    }
  ) \
  .whenNotMatchedInsert(values =
    {
      "driverId": "d3.driverId",
      "dob": "d3.dob",
      "forename": "d3.forename",
      "surname": "d3.surname",
      "createDate": current_timestamp(),
    }
  ) \
  .execute()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.drivers_merge

# COMMAND ----------

