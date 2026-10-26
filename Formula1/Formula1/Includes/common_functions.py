# Databricks notebook source
from pyspark.sql.functions import current_timestamp
def add_ingestion_date(input_df):
    output_df = input_df.withColumn('ingestion_date', current_timestamp())
    return output_df

# COMMAND ----------

def increment_files(files_df, col_id_name, database_name, table_name):
    if col_id_name not in files_df.schema.names:
        print('NOT VALID ID')
        return -1
    
    # This command let us overwrite only the rows with same col_id_name as the table we try to write
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # Append the id column in the last position of the columns
    col_list = [col_name for col_name in files_df.schema.names if col_name != col_id_name]
    col_list.append(col_id_name)
    print(col_list)
    # Select the columns based on the col_list order
    files_df = files_df.select(col_list)
    print(f"{database_name}.{table_name}")
    # Save the table as it is OR increment it to the existing one 
    if (spark._jsparkSession.catalog().tableExists(f"{database_name}.{table_name}")):
        files_df.write.mode('overwrite').insertInto(f"{database_name}.{table_name}")
    else:
        files_df.write.mode('overwrite').partitionBy(col_id_name).format("parquet").saveAsTable(f"{database_name}.{table_name}")
    return 1

# COMMAND ----------

def increment_files_delta(files_df, merge_condition, database_name, table_name, folder_path):
    spark.conf.set("spark.databricks.optimizer.dynamicPartitionPruning", "true")

    if (spark._jsparkSession.catalog().tableExists(f"{database_name}.{table_name}")):
        from delta.tables import DeltaTable
        delta_table = DeltaTable.forPath(spark, f'{folder_path}/{table_name}')
        delta_table.alias(f'{table_name}') \
        .merge(
            files_df.alias('updates'),
            merge_condition
        ) \
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()
    else:
        if 'race_id' in files_df.schema.names:
            files_df.write.mode('overwrite').partitionBy(col_id_name).format("parquet").saveAsTable(f"{database_name}.{table_name}")
        else:
            files_df.write.mode('overwrite').format("delta").saveAsTable(f"{database_name}.{table_name}")
    return 1

# COMMAND ----------

