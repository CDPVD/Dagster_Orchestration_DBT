"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
import dagster as dg
from dagster_dbt import build_schedule_from_dbt_selection

from .assets import CDPVD_dbt_assets

schedules = [
    build_schedule_from_dbt_selection(
         [CDPVD_dbt_assets],
         job_name="CDPVD_DAILY",
         cron_schedule="15 8 * * *",
         dbt_select="fqn:*",
     ),

     dg.ScheduleDefinition(
         name="non_dbt_assets_schedule",
         job_name="non_dbt_assets_job",
         cron_schedule="0 6 * * *",
     ),
]