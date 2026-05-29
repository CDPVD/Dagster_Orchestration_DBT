import dagster as dg

non_dbt_assets_job = dg.define_asset_job(
    name="non_dbt_assets_job", selection="dFondation"
)