from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, hour, unix_timestamp, dayofmonth, dense_rank
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from google.cloud import storage
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


if len(sys.argv) != 4:
    print("Usage: spark-submit script.py <input_csv> <output_csv> bucket_name")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = sys.argv[2]
bucket=sys.argv[3]

spark = SparkSession.builder.appName('ColorMasUsadoPorHora').getOrCreate()
spark.conf.set("spark.sql.session.timeZone", "UTC")

# Read the CSV file and convert timestamp
df = spark.read.option("header", "true").csv(input_csv) \
    .withColumn("timestamp", unix_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss.SSS z").cast(TimestampType())) \
    .withColumn("hour", hour(col("timestamp"))) \
    .withColumn("day", dayofmonth(col("timestamp")))

windowSpec = Window().partitionBy("day", "hour").orderBy(desc("count"))
result_df = df.groupBy("day", "hour", "pixel_color").count() \
    .withColumn("rank", dense_rank().over(windowSpec)) \
    .filter(col("rank") <= 10) \
    .select("day", "hour", "pixel_color", "count") \
    .orderBy("day", "hour", desc("count"), "pixel_color")

# Save the result to the specified output path
#result_df.write.mode("overwrite").csv(output_csv, header=True)

# Filter out rows where 'day', 'hour', or 'pixel_color' is null
result_df = result_df.filter(
    col("day").isNotNull() & col("hour").isNotNull() & col("pixel_color").isNotNull()
)

# Collect the data for plotting
top_colors = result_df.select("day", "hour", "pixel_color", "count").collect()

# Prepare data for plotting
days_hours_colors = [(row.day, row.hour, row.pixel_color, row["count"]) for row in top_colors]

color_series = {}
for day, hour, color, count in days_hours_colors:
    if day!= 1 and hour!=12:
        if color not in color_series:
            color_series[color] = {"x": [], "y": []}

        # Convert day and hour to a single numeric value
        numeric_value = (day - 1) * 24 + hour
        color_series[color]["x"].append(numeric_value)
        color_series[color]["y"].append(count)  # Use count as y-value

# Plotting
plt.figure(figsize=(10, 6))

for color, series in color_series.items():
    # Cambia el color blanco a negro y usa estrellas en lugar de puntos
    rgb_color = mcolors.hex2color(color)
    if color == '#FFFFFF':
        rgb_color = mcolors.hex2color('#F8CFC8')
        marker = '*'
    else:
        marker = 'o'

    plt.plot(series["x"], series["y"], label=color, marker=marker, color=rgb_color)

plt.title('Top 10 Colors Over Time')
plt.xlabel('Time (hours)')
plt.ylabel('Count')
plt.legend()
plt.yscale('log')
plt.grid(True)

# Save the plot locally
local_output_path = '/tmp/day_{}_activity_count.png'.format(day)
plt.savefig(local_output_path)
output_path = 'output/day_{}_activity_count.png'.format(day)  # Adjust the GCS path

# Upload the plot to Google Cloud Storage
upload_blob(bucket, local_output_path, output_path)

# Show the plot
plt.show()