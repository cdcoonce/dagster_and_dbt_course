import os
from dagster_dbt import DbtCliResource

from dagster_and_dbt.defs.project import dbt_project
import boto3
import dagster as dg
from dagster_duckdb import DuckDBResource

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE"),
)

dbt_resource = DbtCliResource(
    project_dir=dbt_project,
)

if os.getenv("DAGSTER_ENVIRONMENT") == "prod":
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    smart_open_config = {"client": session.client("s3")}
else:
    smart_open_config = {}


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": database_resource,
            "dbt": dbt_resource,
        },
    )
