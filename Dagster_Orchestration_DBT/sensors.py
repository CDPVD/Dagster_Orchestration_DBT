import dagster as dg
import smtplib
import configparser
from pathlib import Path


@dg.run_status_sensor(run_status=dg.DagsterRunStatus.FAILURE)
def failure_alert(context: dg.RunFailureSensorContext):
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.joinpath("globalConfigs.cfg").resolve())
        conf = config['alerteCourriel']
        if conf.getboolean('enabled'):
            server = smtplib.SMTP(conf['smtp_server'], conf['smtp_server_port'])
            server.ehlo()
            email_message = f"Subject: Dagster erreur \n\n Le travail: {context.dagster_run.job_name} a echoue."
            server.sendmail(conf['from'], conf['to'], email_message)
            server.quit()