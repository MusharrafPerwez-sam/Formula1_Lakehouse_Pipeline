# Databricks notebook source
# MAGIC %run "../Includes/configuration"

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text("file_date","2021-03-28")
v_file_date = dbutils.widgets.get("file_date")

# COMMAND ----------

results_df_years = spark.read.format("delta").load(f"{presentation_folder_path}/race_results")\
    .filter(f"file_date = '{v_file_date}'")\
    .select(f"race_year")\
    .distinct()\
    .collect()

# COMMAND ----------

results_years = [f'{year[0]}' for year in results_df_years]
print(results_years)

# COMMAND ----------

from pyspark.sql.functions import col
results_df = spark.read.format("delta").load(f"{presentation_folder_path}/race_results")\
    .filter(col('race_year').isin(results_years))

# COMMAND ----------

display(results_df)

# COMMAND ----------

# Group by name and year 
from pyspark.sql.functions import sum, when, col, count, rank, desc
drivers_standings_df = results_df.groupBy('race_year', 'driver_name', 'team')\
                                 .agg(sum('points').alias('total_points'),  count(when(col('position') == 1, True)).alias('wins'))

# COMMAND ----------

from pyspark.sql import Window
window_spec = Window.partitionBy('race_year').orderBy(desc("total_points"))
drivers_standings_df_w_rank = drivers_standings_df.withColumn('rank', rank().over(window_spec))

# COMMAND ----------

display(drivers_standings_df_w_rank.where('race_year=2020'))

# COMMAND ----------

#drivers_standings_df_w_rank.write.mode('overwrite').format("parquet").saveAsTable("f1_presentation.driver_standings")

# COMMAND ----------

#increment_files(drivers_standings_df_w_rank, "race_year", "f1_presentation", "driver_standings")

# COMMAND ----------

increment_files_delta(drivers_standings_df_w_rank, 'driver_standings.race_year = updates.race_year AND driver_standings.driver_name = updates.driver_name AND driver_standings.team = updates.team', 'f1_presentation', 'driver_standings', '/mnt/formula1dlmorales/presentation')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_presentation.driver_standings