from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, concat, lit
import sys

if len(sys.argv) != 3:
    print("Usage: spark-submit script.py <input_csv> <output_txt>")
    sys.exit(1)

input_csv = sys.argv[1]
output_txt = sys.argv[2]

spark = SparkSession.builder.appName('PixelesMasMovidos').getOrCreate()

df = spark.read.option("header", "true").csv(input_csv) \
    .withColumn('cord', col("coordinate")).groupBy("cord").count() \
    .orderBy(desc("count")).limit(10)

df = df.withColumn('result', concat(col('cord'), lit(','), col('count'))).drop('cord', 'count')

# Save the result 
df.select("result").write.mode("overwrite").text(output_txt)
