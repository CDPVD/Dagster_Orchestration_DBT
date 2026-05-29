import os
from snowflake.connector import connect
import dagster as dg
import pandas as pd
from .dFondationConfigs import dfondation
import configparser
from datetime import datetime

@dg.asset
def dFondation():
    config = configparser.ConfigParser()
    config.read('.\\Dagster_Orchestration_DBT\\globalConfigs.cfg')
    dFondationSettings = config['dFondation']
    errorLogger = []
    if dFondationSettings.getboolean('enabled'):
        for schemaName, conf in dfondation.items():
            try:
                extractSchema(conf, dFondationSettings)
            except Exception as e:
                errorLogger.append(e)
                continue
    
    if len(errorLogger) > 0:
        raise errorLogger[0]


def extractSchema(conf: dict, dFondationSettings: list):
    connection = connect(
        user=dFondationSettings["user"],
        #Si le mot de passe n'est pas dans une variable d'environnement, on assume que le mot de passe est en "clair" dans la config
        password=os.getenv(dFondationSettings["password"],dFondationSettings["password"]),
        account=dFondationSettings["account"],
        warehouse=dFondationSettings["warehouse"],
        database=dFondationSettings["database"],
        schema=conf["schema"],
        role=conf["role"]
    )

    cur = connection.cursor()
    
    for tableName, fields in conf["tables"].items():
        data = cur.execute("SELECT " + fields + " FROM " + tableName).fetch_pandas_all().replace(';','',regex=True)
        dateTimeStamped = data.assign(extractDate=datetime.today().strftime('%Y-%m-%d'))
        dateTimeStamped.to_csv(dFondationSettings['pathPreFix'] + tableName + ".csv", sep=';', index=False, header=True)
    
    connection.close()