"""
Code that goes along with the Airflow tutorial located at:
https://github.com/airbnb/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Will show up under airflow.operators.test_plugin.PluginOperator
from airflow.operators.aws_glue_plugin import AWSGlueJobOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('tutorial_xignite', default_args=default_args)
"""
Run xignite into S3
- two operators dependent
- branch elasticsearch tasks
- branch mysql job
"""


# t1, t2 and t3 are examples of tasks created by instantiating operators
# t1 = DockerOperator(
#     task_id='get_xignite_exchanges',
#     image='xignite_fundamentals',
#     command='make',
#     start_date=datetime(2018, 5, 10))
t1 = BashOperator(
    task_id='get_xignite_exchanges',
    bash_command='cd /Users/akeating/go/src/github.com/cbinsights/xignite-raw-fundamentals-job && make -f Makefyle MODE="exchanges"',
    retries=1,
    dag=dag)

t2 = BashOperator(
    task_id='get_xignite_companies',
    bash_command='cd /Users/akeating/go/src/github.com/cbinsights/xignite-raw-fundamentals-job && make -f Makefyle MODE="companies"',
    retries=1,
    dag=dag)

t3 = BashOperator(
    task_id='get_xignite_fundamentals_list',
    bash_command='cd /Users/akeating/go/src/github.com/cbinsights/xignite-raw-fundamentals-job && make -f Makefyle MODE="fundamentalslist"',
    retries=1,
    dag=dag)

# Not implemented
# t4 = BashOperator(
#     task_id='load_xignite_fundamentals_list',
#     bash_command='cd /Users/akeating/go/src/github.com/cbinsights/xignite-raw-fundamentals-job && make -f Makefyle MODE="loadfundamentals"',
#     retries=1,
#     dag=dag)

# t5 = AWSGlueJobOperator(job_name='mysql_to_s3_xignite2',
#                         concurrent_run_limit=1,
#                         script_location='s3://com.cbinsights.raw-datastore-us-east-1/glue-scripts/xignite_mysql_to_s3',
#                         retry_limit=1,
#                         num_of_dpus=10,
#                         region_name='us-east-1',
#                         s3_bucket='glue-scripts',
#                         iam_role_name='aws-glue-role',
#                         task_id='xignite_mysql_to_s3',
#                         start_date=datetime(2018, 5, 10))

t2 << t1
t3 << t1
# t5 << t2
# t5 << t3