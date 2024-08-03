from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

dag = DAG(
    dag_id='pipeline2_dag',
    default_args=default_args,
    start_date=datetime(2024, 1, 9),  # Replace with your desired start date
    catchup=False,
    schedule_interval=None,  # This DAG is triggered by pipeline1_dag
)

t2 = BashOperator(
    task_id='run_pipeline2',
    bash_command='python $AIRFLOW_HOME/dags/scripts/main.py',
  dag=dag,
)

t2