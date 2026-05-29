from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import CDPVD_dbt_assets
from .non_dbt_assets.dFondation import dFondation
from .project import CDPVD_project
from .jobs import non_dbt_assets_job
from .schedules import schedules
from .sensors import failure_alert

defs = Definitions(
    assets=[CDPVD_dbt_assets, dFondation],
    schedules=schedules,
    jobs=[non_dbt_assets_job],
    sensors=[failure_alert],
    resources={
        "cdpvd": DbtCliResource(project_dir=CDPVD_project),
    },
)