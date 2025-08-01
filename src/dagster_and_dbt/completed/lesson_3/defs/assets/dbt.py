import dagster as dg
from dagster_dbt import DbtCliResource, dbt_assets

from dagster_and_dbt.completed.lesson_3.defs.project import dbt_project


@dbt_assets(
    manifest=dbt_project.manifest_path,
)
def dbt_analytics(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()
