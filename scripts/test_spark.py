import os
from pyspark.sql import SparkSession

# --- Environment Setup ---
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-23"
os.environ["HADOOP_HOME"] = r"D:\old data\DESKTOP\hadoop"
os.environ["hadoop.home.dir"] = r"D:\old data\DESKTOP\hadoop"
os.environ["PYSPARK_PYTHON"] = "python"

print("JAVA_HOME =", os.environ["JAVA_HOME"])
print("HADOOP_HOME =", os.environ["HADOOP_HOME"])

# --- Spark Session ---
spark = (
    SparkSession.builder
    .appName("TestSpark")
    .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow")
    .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")
print("✅ Spark initialized successfully!")

# --- Small DataFrame Test ---
data = [(1, "Ashmitha"), (2, "Reddy"), (3, "Thota")]
df = spark.createDataFrame(data, ["id", "name"])
df.show()
