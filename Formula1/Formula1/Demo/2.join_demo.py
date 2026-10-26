# Databricks notebook source
# MAGIC %run "../Includes/configuration"

# COMMAND ----------

races_df = spark.read.parquet(f"{processed_folder_path}/races").filter("race_year = 2019")
display(races_df)

# COMMAND ----------

circuits_df = spark.read.parquet(f"{processed_folder_path}/circuits")\
                        .filter("circuit_id < 70")
display(circuits_df)

# COMMAND ----------

circuits_df = circuits_df.withColumnRenamed('name', 'circuit_name')
races_df = races_df.withColumnRenamed('name', 'race_name')

# COMMAND ----------

race_circuits_df = circuits_df.join(races_df, circuits_df.circuit_id == races_df.circuit_id, "inner")\
                              .select(circuits_df.circuit_id, circuits_df.circuit_name, circuits_df.location, circuits_df.country, races_df.race_name, races_df.round)

# COMMAND ----------

display(race_circuits_df)

# COMMAND ----------

left_join_circuits = circuits_df.join(races_df, circuits_df.circuit_id == races_df.circuit_id, "leftouter")

# COMMAND ----------

display(left_join_circuits)
display(left_join_circuits.filter("race_id is NULL").count())

# COMMAND ----------

right_join_circuits = circuits_df.join(races_df, circuits_df.circuit_id == races_df.circuit_id, "rightouter")

# COMMAND ----------

display(right_join_circuits)
display(right_join_circuits.filter("circuit_ref is NULL").count())

# COMMAND ----------

full_join_circuits = circuits_df.join(races_df, circuits_df.circuit_id == races_df.circuit_id, "fullouter")

# COMMAND ----------

display(full_join_circuits)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Semi Join : Like inner join but returns only the left side table columns

# COMMAND ----------

semi_join_circuits = circuits_df.join(races_df, circuits_df.circuit_id == races_df.circuit_id, "semi")
display(semi_join_circuits)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Anti Join : Opposite of semi join

# COMMAND ----------

anti_join_circuits = circuits_df.join(races_df, circuits_df.circuit_id == races_df.circuit_id, "anti")
display(anti_join_circuits)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Cross Join

# COMMAND ----------

races_circuits_df = races_df.crossJoin(circuits_df)
display(races_circuits_df)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /mnt/formula1dlmorales/

# COMMAND ----------

