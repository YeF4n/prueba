from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, concat, lit
import sys

if len(sys.argv) != 3:
    print("Usage: spark-submit script.py <input_csv> <output_txt>")
    sys.exit(1)

input_csv = sys.argv[1]
output_txt = sys.argv[2]

spark = SparkSession.builder.appName('UsserMasActivo').getOrCreate()

df = spark.read.option("header", "true").csv(input_csv) \
    .withColumn('id', col("user_id")).groupBy("id").count().orderBy(desc("count"))

# Only select the top 10 users
df_top10 = df.limit(10)

df_top10 = df_top10.withColumn('result', concat(col('id'), lit(','), col('count'))).drop('id', 'count')

# Save the result
df_top10.write.mode("overwrite").text(output_txt)
