from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import matplotlib.pyplot as plt
import sys
from google.cloud import storage

def process_and_plot_data(file_path, output_path, bucket):
    spark = SparkSession.builder.appName('Color').getOrCreate()

    #Lectura de los datos
    df = spark.read.option("header", "true").csv(file_path) \
        .withColumn('color', col("pixel_color")).groupBy("color").count()
    data = df.collect()

    # Sacamos cada dato de la coordinada (X el pixel e Y las veces que aparece)
    pixel_colors = [row["color"] for row in data]
    counts = [row["count"] for row in data]

    # Dibuja grafica
    plt.bar(pixel_colors, counts, color=pixel_colors, edgecolor='black')
    plt.xlabel('Pixel Color')
    plt.ylabel('Count')
    plt.title('Count of Each Pixel Color')
    plt.xticks(rotation=45, ha='right')  # Rotating x-axis labels for better visibility
    
    # Guardado local
    local_output_path = "/tmp/output.png"
    plt.savefig(local_output_path)
    plt.close()
    print("Plot saved as {}".format(local_output_path))

    #Guardado nube
    upload_blob(bucket, local_output_path, output_path)

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
        print("Usage: python script.py <csv_file_path> <output_image_path> bucket_name")
        sys.exit(1)

    file_path = sys.argv[1]
    output_image_path = sys.argv[2]
    bucket=sys.argv[3]
    process_and_plot_data(file_path, output_image_path, bucket)
