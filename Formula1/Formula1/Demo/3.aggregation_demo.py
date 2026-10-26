# Databricks notebook source
# MAGIC %run "../Includes/configuration"

# COMMAND ----------

race_results_df = spark.read.parquet(f"{presentation_folder_path}/race_results")


# COMMAND ----------

display(race_results_df)

# COMMAND ----------

demo_df = race_results_df.filter("race_year = 2020")

# COMMAND ----------

display(demo_df)

# COMMAND ----------

from pyspark.sql.functions import count, countDistinct, sum


# COMMAND ----------

demo_df.select(countDistinct('race_name')).show()

# COMMAND ----------

demo_df.select(sum('points')).show()

# COMMAND ----------

demo_df.filter('driver_name = "Lewis Hamilton"').select(sum('points'), countDistinct('race_name'))\
    .withColumnRenamed('sum(points)', 'total_points')\
        .withColumnRenamed('count(DISTINCT race_name)', 'total_races')\
            .show()

# COMMAND ----------

# Doesn't work
#demo_df.groupBy('driver_name')\
#       .sum("points")\
#        .countDistinct("race_name")\
#         .show()


# COMMAND ----------

demo_df.groupBy('driver_name')\
    .agg(sum("points").alias("total_points"), countDistinct("race_name").alias("total_races_run"))\
        .show()

# COMMAND ----------

demo_df = race_results_df.filter("race_year in (2019, 2020)")
display(demo_df)

# COMMAND ----------

from pyspark.sql.functions import desc
demo_grouped_df = demo_df.groupBy('race_year', 'driver_name')\
        .agg(sum('points').alias("total_points"), countDistinct('race_name').alias("total_race_run"))

# COMMAND ----------

from pyspark.sql.functions import desc, rank
from pyspark.sql.window import Window

driverRankSpec = Window.partitionBy("race_year").orderBy(desc("total_points"))
demo_grouped_df.withColumn("rank", rank().over(driverRankSpec)).show(100)

# COMMAND ----------

