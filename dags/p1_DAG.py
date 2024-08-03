from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import pytz

def trigger_pipeline2_if_time_right(*args, **kwargs):
    # Get current time in UTC
    now = datetime.utcnow()
    # Check if current time is within the 8 PM hour
    if now.hour == 20:
        return 'trigger_pipeline2'
    else:
        # If not the correct time, skip the triggering
        return 'skip_trigger'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

dag = DAG(
    dag_id='pipeline1_dag',
    default_args=default_args,
    start_date=datetime(2024, 1, 9),  # Replace with your desired start date
    catchup=False,
    schedule_interval='0 19 * * *',  # Runs at 7 PM every day
)

t1 = BashOperator(
    task_id='run_pipeline1',
    bash_command='python $AIRFLOW_HOME/dags/scripts/pipeline1.py',
    dag=dag,
)

check_time = PythonOperator(
    task_id='check_time',
    python_callable=trigger_pipeline2_if_time_right,
    provide_context=True,
    dag=dag,
)

trigger_pipeline2 = TriggerDagRunOperator(
    task_id='trigger_pipeline2',
    trigger_dag_id='pipeline2_dag',  # The ID of the DAG to trigger
    dag=dag,
)

skip_trigger = EmptyOperator(
    task_id='skip_trigger',
    dag=dag,
)

# Task dependencies
t1 >> check_time
check_time >> [trigger_pipeline2, skip_trigger]