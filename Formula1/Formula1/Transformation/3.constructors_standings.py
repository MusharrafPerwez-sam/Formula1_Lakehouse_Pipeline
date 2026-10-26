# Databricks notebook source
# MAGIC %run "../Includes/configuration"

# COMMAND ----------

# MAGIC %run "../Includes/common_functions"

# COMMAND ----------

dbutils.widgets.text('file_date', '2021-03-28')
v_file_date = dbutils.widgets.get('file_date')

# COMMAND ----------

results_years_df = spark.read.format("delta").load(f"{presentation_folder_path}/race_results")\
    .filter(f"file_date = '{v_file_date}'")\
    .select("race_year")\
    .distinct()\
    .collect()

# COMMAND ----------

result_years_list = [year[0] for year in results_years_df]

# COMMAND ----------

from pyspark.sql.functions import col
results_df = spark.read.format("delta").load(f"{presentation_folder_path}/race_results")\
    .filter(col('race_year').isin(result_years_list))

# COMMAND ----------

# aggregation first
from pyspark.sql.functions import sum, count, when, desc, rank
agg_results_df = results_df.groupBy("team", "race_year")\
                            .agg(sum("points").alias("total_points"), count(when(results_df.position == 1, True)).alias("wins"))

# COMMAND ----------

display(agg_results_df)

# COMMAND ----------

from pyspark.sql import Window
window_spec = Window.partitionBy("race_year").orderBy(desc("total_points"))
final_results_df = agg_results_df.withColumn('rank', rank().over(window_spec))

# COMMAND ----------

display(final_results_df.where('race_year=2020'))

# COMMAND ----------

#increment_files(final_results_df, "race_year", "f1_presentation", "constructors_standings")

# COMMAND ----------

increment_files_delta(final_results_df, 'constructors_standings.team = updates.team AND constructors_standings.race_year = updates.race_year', 'f1_presentation', 'constructors_standings', '/mnt/formula1dlmorales/presentation')

# COMMAND ----------

#final_results_df.write.mode('overwrite').format("parquet").saveAsTable("f1_presentation.constructors_standings")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_presentation.constructors_standings