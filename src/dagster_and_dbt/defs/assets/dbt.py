import dagster as dg
import json

from dagster_dbt import dbt_assets, DbtCliResource
from ..partitions import daily_partition
from defs.project import dbt_project
from dagster_dbt import DagsterDbtTranslator
from dagster import AssetKey


INCREMENTAL_SELECTOR = "config.materialized:incremental"

class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return dg.AssetKey(f"taxi_{name}")
        else:
            return super().get_asset_key(dbt_resource_props)
        
    def get_group_name(self, dbt_resource_props):
        return dbt_resource_props["fqn"][1]


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    exclude=INCREMENTAL_SELECTOR
)
def dbt_analytics(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    select=INCREMENTAL_SELECTOR,
    partitions_def=daily_partition
)
def incremental_dbt_models(
    context: dg.AssetExecutionContext,
    dbt: DbtCliResource
):
    time_window = context.partition_time_window
    dbt_vars = {
        "min_date": time_window.start.strftime('%Y-%m-%d'),
        "max_date": time_window.end.strftime('%Y-%m-%d')
    }

    yield from dbt.cli(["build", "--vars", json.dumps(dbt_vars)], context=context).stream()


