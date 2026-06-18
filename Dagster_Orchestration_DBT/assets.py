import dagster as dg
import smtplib
import os
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
    dbt_target = os.environ["DBT_TARGET"]
    yield from cdpvd.cli(
        ["compile", "--target", dbt_target],
        context=context,
    ).stream()

    yield from cdpvd.cli(
        ["seed", "--target", dbt_target, "--full-refresh"],
        context=context,
    ).stream()

    yield from cdpvd.cli(
        ["run", "--target", dbt_target],
        context=context,
    ).stream()

    yield from cdpvd.cli(
        ["test", "--target", dbt_target],
        context=context,
    ).stream()