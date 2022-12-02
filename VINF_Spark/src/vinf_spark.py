
import pyspark                                          # type: ignore
from pyspark.sql.types import ArrayType, FloatType, StructField, StructType, StringType, IntegerType, DecimalType   # type: ignore
from pyspark import SparkConf, SparkContext, SQLContext # type: ignore
from pyspark.sql import SparkSession                    # type: ignore

import os

class DataManager:
    def __init__(self):
        pass

    def read_json_into_df(spark_session, filename):
        df = None
        return df

if __name__ == "__main__":
    spark_conf = SparkConf().setAppName("VINF Spark").setMaster("local")

    spark_conf.set("spark.executor.memory", "3g")
    spark_conf.set("spark.driver.memory", "3g")
    spark_conf.set("spark.cores.max", "4")

    spark_context = SparkContext(conf=spark_conf)
    spark_session = SparkSession.builder.getOrCreate()

    schema = StructType([
        StructField('title', StringType(), True),
        StructField('categories', StringType(), True),
        StructField('birth_date', StringType(), True),
        StructField('birth_date_is_bc', StringType(), True),
        StructField('death_date', StringType(), True),
        StructField('death_date_is_bc', FloatType(), True),
        StructField('birth_place', FloatType(), True),
        StructField('death_place', FloatType(), True)
    ])
    pass

