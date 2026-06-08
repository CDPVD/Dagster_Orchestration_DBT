import dagster as dg
import smtplib
from typing import Any, Mapping
from dagster import AssetKey, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator

from .project import CDPVD_project

class CDPVDDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        return super().get_asset_key(dbt_resource_props).with_prefix("CDPVD")
    
@dbt_assets(manifest=CDPVD_project.manifest_path,
    dagster_dbt_translator=CDPVDDagsterDbtTranslator(),
    )
def CDPVD_dbt_assets(context: AssetExecutionContext, cdpvd: DbtCliResource):
    yield from cdpvd.cli(
        ["build", "--target", "dev"],  # ou prod, staging...
        context=context
        ).stream()

 