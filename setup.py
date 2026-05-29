from setuptools import find_packages, setup

setup(
    name="Dagster_Orchestration_DBT",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "Dagster_Orchestration_DBT": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-sqlserver<1.10",
        "dbt-sqlserver<1.10",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)