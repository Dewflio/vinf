import pyspark           # type: ignore                              
from pyspark.sql.types import ArrayType, FloatType, StructField, StructType, StringType, IntegerType, DecimalType # type: ignore
from pyspark import SparkConf, SparkContext, SQLContext # type: ignore
from pyspark.sql import SparkSession            # type: ignore 
import pyspark.sql.functions as F               # type: ignore


import os
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

from vinf_parser import VINF_Parser
page_parser = VINF_Parser()


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

schema = StructType([
    StructField('title', StringType(), True),
    StructField('categories', StringType(), True),
    StructField('birth_date', StringType(), True),
    StructField('birth_date_is_bc', StringType(), True),
    StructField('death_date', StringType(), True),
    StructField('death_date_is_bc', StringType(), True),
    StructField('birth_place', StringType(), True),
    StructField('death_place', StringType(), True)
])


parse_records_udf = F.udf(lambda x: page_parser.parse_record(x), schema)

df = spark.read.option("multiline","true").json(root_folder + '/data/parsed_pages.json')

df.show(n=10, truncate=True)

newDF = (
    df
    .withColumn("Output", parse_records_udf(df["page"]))
    .select("Output.*")
)

newDF.show(n=10, truncate=True)
newDF.explain()

#newDF.write.format('json').save(root_folder + "/data/records_spark.json")

newDF.write.json(root_folder + "/spark_output")

