import configparser
from pathlib import Path
from dagster_dbt import DbtProject

config = configparser.ConfigParser()
config.read(Path(__file__).parent.joinpath("globalConfigs.cfg").resolve())
conf = config['base']

CDPVD_project = DbtProject(
    project_dir=Path(__file__).joinpath("..","..","..",conf['dbtProjectPath'], conf['dbtProjectName']).resolve(),
    packaged_project_dir=Path(__file__).joinpath("..","..","..", conf['dbtProjectPath'], "dbt-project").resolve(),
)
CDPVD_project.prepare_if_dev()