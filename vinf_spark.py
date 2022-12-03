import findspark
findspark.init()

import pyspark                                         
from pyspark.sql.types import ArrayType, FloatType, StructField, StructType, StringType, IntegerType, DecimalType
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession                   
import os
import sys
import logging

#define the root folder so that python recognises packages
spark_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(spark_folder)))
sys.path.append(root_folder)

print(sys.path)

from vinf_parser import VINF_Parser

class DataManager:
    def __init__(self):
        ok = True
        pass

    def read_json_into_df(spark_session, filename):
        df = None
        return df

if __name__ == "__main__":
    #logging settig - INFO
    logging.basicConfig(level=logging.INFO)

    logging.info("setting up spark config")
    spark_conf = SparkConf().setAppName("VINF Spark").setMaster("local")

    spark_conf.set("spark.executor.memory", "3g")
    spark_conf.set("spark.driver.memory", "3g")
    spark_conf.set("spark.cores.max", "4")

    logging.info("setting up spark context")
    spark_context = SparkContext(conf=spark_conf)
    logging.info("setting up spark session")
    spark_session = SparkSession.builder.getOrCreate()
    logging.info("Spark config, context and session are set up")

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
    pass
