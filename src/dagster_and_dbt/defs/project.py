from pathlib import Path

from dagster_dbt import DbtProject


dbt_project = DbtProject(
  project_dir=Path(__file__).joinpath("../..", "analytics").resolve(),
)

dbt_project.prepare_if_dev()
