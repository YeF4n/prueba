import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, unix_timestamp, dayofmonth, count, first
from pyspark.sql.types import TimestampType
import matplotlib.pyplot as plt
from google.cloud import storage

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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <csv_file> <output_folder> bucket_name")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_folder = sys.argv[2]
    bucket=sys.argv[3]

    spark = SparkSession.builder.appName('horasMasActividad').getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "UTC")

    df = spark.read.option("header", "true").csv(csv_file) \
        .withColumn("timestamp", unix_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss.SSS z").cast(TimestampType())) \
        .withColumn("hour", hour(col("timestamp"))) \
        .withColumn("day", dayofmonth(col("timestamp"))) \
        .groupBy("day", "hour").agg(first("timestamp").alias("timestamp"), count("*").alias("activity_count")) \
        .orderBy("day", "hour")


    data = df.collect()

    for day in set([row["day"] for row in data]):
        if day is not None:
            day_data = [row for row in data if row["day"] == day]
            hours = [row["hour"] for row in day_data]
            counts = [row["activity_count"] for row in day_data]

            all_hours = list(range(24))
            counts_filled = [counts[hours.index(hour)] if hour in hours else 0 for hour in all_hours]

            plt.bar(all_hours, counts_filled)
            plt.xlabel('Hour of day {}'.format(day_data[0]["timestamp"].strftime("%Y/%m/%d")))
            plt.ylabel('Count')
            plt.title('Count of Activities per Hour - Day' )

            # Save the plot locally
            local_output_path = '/tmp/day_{}_activity_count.png'.format(day)
            plt.savefig(local_output_path)

            plt.close()
            
            output_path = 'output/day_{}_activity_count.png'.format(day)
            upload_blob(bucket, local_output_path, output_path)


            
