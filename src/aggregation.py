from pyspark.sql import SparkSession
import json
from pyspark.sql.types import StructType, DataType, MapType, StructType, StructField, StringType, IntegerType, ArrayType, FloatType, BooleanType, LongType, DoubleType
from pyspark.sql.functions import from_json, col

scala_version = '2.12'
spark_version = '3.3.1'
# TODO: Ensure match above values match the correct versions
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1'
]

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("SparkKafkaStreaming") \
        .master("local") \
        .config("spark.jars.packages", ",".join(packages)) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    json_data = """{
  "id": "e581d976-b2f9-4d8d-9340-65baad4f33be",
  "restaurant": "43.499.665/2594-24",
  "customer": "178.903.878-22",
  "state": "RJ",
  "total_value": 327.95,
  "items": [
    {
      "item": 1,
      "dish": "Cachorro Quente Ao Molho",
      "spices": "Especiaria",
      "vegetable": "Catalônia",
      "fruit": "Pêra",
      "drink": "Magna",
      "price": "R$63.61",
      "quantity": 2,
      "total": "R$127.22"
    },
    {
      "item": 2,
      "dish": "Paleta De Carneiro",
      "spices": "Alho",
      "vegetable": "couve-rábano",
      "fruit": "Mirtilo",
      "drink": "Imperial",
      "price": "R$87.75",
      "quantity": 1,
      "total": "R$87.75"
    },
    {
      "item": 3,
      "dish": "Purê De Batata",
      "spices": "Pimenta-do-reino",
      "vegetable": "Pepino",
      "fruit": "Amoras",
      "drink": "Coral",
      "price": "R$12.84",
      "quantity": 1,
      "total": "R$12.84"
    },
    {
      "item": 4,
      "dish": "Açaí",
      "spices": "Canela",
      "vegetable": "Semente de lótus",
      "fruit": "Medronheiro",
      "drink": "Magna",
      "price": "R$33.38",
      "quantity": 3,
      "total": "R$100.14"
    }
  ],
  "payment_method": "money",
  "updated_at": "2022-10-27T22:44:57.764718",
  "status_code": 4169,
  "lucky_cookie": "O prazer de concretizar seus projetos com toda a tranquilidade"
}"""
    # df = spark.read.json(spark.sparkContext.parallelize([json_data]))
    # print(df.schema.json())
    # new_schema = StructType.fromJson(json.loads(df.schema.json()))
    # print(new_schema)

    schema = StructType([StructField('customer', StringType(), True), StructField('id', StringType(), True),
                         StructField('items', ArrayType(StructType(
                             [StructField('dish', StringType(), True), StructField('drink', StringType(), True),
                              StructField('fruit', StringType(), True), StructField('item', LongType(), True),
                              StructField('price', StringType(), True), StructField('quantity', LongType(), True),
                              StructField('spices', StringType(), True), StructField('total', StringType(), True),
                              StructField('vegetable', StringType(), True)]), True), True),
                         StructField('lucky_cookie', StringType(), True),
                         StructField('payment_method', StringType(), True),
                         StructField('restaurant', StringType(), True), StructField('state', StringType(), True),
                         StructField('status_code', LongType(), True), StructField('total_value', DoubleType(), True),
                         StructField('updated_at', StringType(), True)])

    nestTimestampFormat = "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"
    jsonOptions = {"timestampFormat": nestTimestampFormat}
    # Read from kafka topic

    # df = (
    #     spark.readStream.format("kafka")
    #     .option("kafka.bootstrap.servers", "localhost:9092")
    #     .option("subscribe", "customer-order")
    #     .load()
    #     .select(from_json(col("value").cast("string"), schema, jsonOptions).alias("parsed_value"))
    # )
    #
    # # Print the schema for the incoming kafka message
    # df.printSchema()
    #
    # # Write the incoming kafka message to console
    # query = (
    #     df.writeStream.format("console")
    #     .outputMode("append")
    #     .option("truncate", "false")
    #     .start()
    # )

    lines = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "customer-order") \
        .load() \
        #.select(from_json(col("value").cast("string"), schema, jsonOptions).alias("parsed_value"))

    Casted = lines.select(from_json(col("value").cast("string"), schema, jsonOptions).alias("parsed_value"))

    new_df = Casted.select("parsed_value.*")

    df1 = new_df.select("id", "restaurant", "customer", "state", "total_value", "items", "payment_method", "updated_at", "status_code", "lucky_cookie")

    query = (
        df1.writeStream.format("console")
        .outputMode("append")
        .option("truncate", "false")
        .start()
    )

    # get timestamp from kafka message
    df = lines.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")


    query.awaitTermination()

    # df1 = new_df.select(col("type"), col("country"), col("invoice_no"), col("timestamp"), explode(col("items")))

#
# spark = SparkSession \
#     .builder \
#     .appName("CustomerOrderStream") \
#     .getOrCreate()
#
# # get the streaming data from kafka
# customer_order_stream = spark \
#     .readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092,localhost:9093,localhost:9094") \
#     .option("subscribe", "customer-order") \
#     .option("startingOffsets", "earliest") \
#     .option("failOnDataLoss", "false") \
#     .load()
#
# # create a dataframe with the values
# customer_order_df = customer_order_stream.selectExpr("CAST(value AS STRING)")
#
# # create a temporary view to make the SQL queries
# customer_order_df.createOrReplaceTempView("customer_order")
#
# # query the data
# customer_order_query = customer_order_df \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()
#
# customer_order_query.awaitTermination()