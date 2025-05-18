# dags/etl_dag.py
from datetime import datetime, timedelta
from airflow.decorators import dag, task
import subprocess
import logging

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

logger = logging.getLogger("airflow.etl")
logger.setLevel(logging.INFO)

@dag(
    dag_id='fire_incidents_etl',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily',
    catchup=False,
    description='ETL completo para ingestão de dados de incidentes de incêndio'
)
def fire_incidents_dag():

    @task()
    def extract():
        try:
            subprocess.run(["python", "etl/extract.py"], check=True)
            logger.info("Extração concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro na extração: {e}")
            raise

    @task()
    def transform():
        try:
            subprocess.run(["python", "etl/transform.py"], check=True)
            logger.info("Transformação concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro na transformação: {e}")
            raise

    @task()
    def load():
        try:
            subprocess.run(["python", "etl/load.py"], check=True)
            logger.info("Carga concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro na carga: {e}")
            raise

    @task()
    def run_dbt():
        try:
            subprocess.run(["dbt", "run", "--project-dir", "dbt"], check=True)
            logger.info("Execução do DBT concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao executar DBT: {e}")
            raise

    e = extract()
    t = transform()
    l = load()
    d = run_dbt()

    e >> t >> l >> d

etl_pipeline = fire_incidents_dag()
