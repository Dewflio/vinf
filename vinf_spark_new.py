import pyspark           # type: ignore                              
from pyspark.sql.types import ArrayType, FloatType, StructField, StructType, StringType, IntegerType, DecimalType # type: ignore
from pyspark import SparkConf, SparkContext, SQLContext # type: ignore
from pyspark.sql import SparkSession            # type: ignore 
import pyspark.sql.functions as F               # type: ignore

from pyspark.sql.column import Column, _to_java_column   # type: ignore
from pyspark.sql.types import _parse_datatype_json_string    # type: ignore


import os
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

from vinf_parser import VINF_Parser
page_parser = VINF_Parser()

input_xmls = os.listdir(root_folder + "/data/input_xmls_unpacked")
paths = []
for file in input_xmls:
    paths.append(root_folder + "/data/input_xmls_unpacked/" + file)
print(paths)

'''
spark = SparkSession.builder.config(
    conf=(
        SparkConf()
        .setAppName("My-Spark-Application")
        .setMaster("local[*]")
        # .setMaster("spark://spark-master:7077")
        .set("spark.files.overwrite", "true")
        .set("spark.dynamicAllocation.enabled", "true")
        .set("spark.dynamicAllocation.minExecutors","1")
        .set("spark.dynamicAllocation.maxExecutors","4")
        .set("spark.executor.memory", "4g")
        .set("spark.executor.cores", "2")
        .set("spark.driver.memory", "8g")
        .set("spark.driver.cores", "1")
        .set("spark.cores.max", "8")
    )
).getOrCreate()
'''

spark = SparkSession.builder.master("local[*]")\
        .config('spark.jars.packages', 'com.databricks:spark-xml_2.12:0.15.0')\
        .getOrCreate()

schema = StructType([
    StructField('title', StringType(), True),
    StructField('categories', StringType(), True),
    StructField('name', StringType(), True),
    StructField('birth_date', StringType(), True),
    StructField('birth_date_is_bc', StringType(), True),
    StructField('death_date', StringType(), True),
    StructField('death_date_is_bc', StringType(), True),
    StructField('birth_place', StringType(), True),
    StructField('death_place', StringType(), True)
])

schema_xml = StructType([
        StructField('title', StringType(), True),
        StructField('revision', StructType([
            StructField('text', StringType(), True),
        ]))
    ])

df = spark.read \
        .format('com.databricks.spark.xml') \
        .options(rowTag="page") \
        .load(",".join(paths), schema=schema_xml)

df.show(n=10, truncate=True)

df = df.where(df["revision"]["text"].contains("birth_date"))
df.show(n=10, truncate=True)

#udf to parse the record
parse_records_udf = F.udf(lambda x, y: page_parser.parse_record_new(x, y), schema)

newDF = (
    df
    .withColumn("Output", parse_records_udf(df["title"], df["revision"]["text"]))
    .select("Output.*")
)

newDF.show(n=10, truncate=True)
newDF.explain()

newDF.write.json(root_folder + "/spark_output_new")

