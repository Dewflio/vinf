import pyspark.sql.functions as F   # type: ignore
import pyspark.sql.types as T   # type: ignore

from pyspark.sql import SparkSession    # type: ignore
spark = SparkSession.builder.appName("Test Of Requests").getOrCreate()

df = spark.createDataFrame([("Alive", 4)], ["Name", "Number"])


def example(n):
    return {'Out1':n+2, 'Out2': n-2}


SCHEMA = T.StructType([
    T.StructField("Out1", T.IntegerType(), False),
    T.StructField("Out2", T.IntegerType(), False)
])

example_udf = F.udf(lambda x: example(x), SCHEMA)

newDF = (
    df
    .withColumn("Output", example_udf(df["Number"]))
    .select('Name', 'Number',"Output.*")
)

newDF.show(truncate=False)
newDF.explain()