import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ["JOB_NAME", "TempDir", "Stage"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon S3
AmazonS3_node1701168142582 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://luk-source-{stage}/school/".format(stage=args['Stage'])]},
    transformation_ctx="AmazonS3_node1701168142582",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1701168225063 = DynamicFrame.fromDF(
    AmazonS3_node1701168142582.toDF().dropDuplicates(["teacher_id"]),
    glueContext,
    "DropDuplicates_node1701168225063",
)

school_source_node1700125451889 = glueContext.create_dynamic_frame.from_options(
    connection_type="redshift",
    connection_options={
        "dbtable": "school",
        "redshiftTmpDir": args['TempDir'],
        "useConnectionProperties": "true",
        "connectionName": "luk-data-glue-red",
    },
)

# Script generated for node Amazon S3
AmazonS3_node1699455302913 = glueContext.write_dynamic_frame.from_options(
    frame=DropDuplicates_node1701168225063,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://luk-data-lake-{stage}/school/teacher/".format(stage=args['Stage']), "partitionKeys": []},
    format_options={"compression": "snappy"}
)

# Script generated for node SQL Query
SqlQuery0 = """
select  CAST(t.teacher_id AS BIGINT) teacher_id, 
        t.name, 
        (select MIN(s.school_id) from s where s.school_code = t.school_code) school_id,
from t;
"""
SQLQuery_node1700125451889 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "t": DropDuplicates_node1701168225063,
        "s":school_source_node1700125451889
    },
    transformation_ctx="SQLQuery_node1700125451889",
)

# Script generated for node Amazon Redshift
AmazonRedshift_node1701168534140 = glueContext.write_dynamic_frame.from_options(
    frame=SQLQuery_node1700125451889,
    connection_type="redshift",
    connection_options={
        "postactions": """BEGIN; MERGE INTO teacher USING temp_teacher ON teacher.teacher_id = temp_teacher.teacher_id WHEN MATCHED THEN UPDATE SET teacher_id = temp_teacher.teacher_id, name = temp_teacher.name, school_id = temp_teacher.school_idWHEN NOT MATCHED THEN INSERT VALUES (temp_teacher.teacher_id, temp_teacher.name, temp_teacher.school_id); DROP TABLE temp_teacher; END;""",
        "redshiftTmpDir": args['TempDir'],
        "useConnectionProperties": "true",
        "dbtable": "temp_teacher",
        "connectionName": "luk-data-glue-red",
        "preactions": """CREATE TABLE IF NOT EXISTS teacher (teacher_id BIGINT, name VARCHAR, school_id INTEGER);  DROP TABLE IF EXISTS temp_teacher; CREATE TABLE temp_teacher(teacher_id BIGINT, name VARCHAR, school_id INTEGER);""",
    },
    transformation_ctx="AmazonRedshift_node1701168534140",
)

job.commit()
