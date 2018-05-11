# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

# Importing base classes that we need to derive
from aws_glue.aws_glue_job_operator import AWSGlueJobOperator
from aws_glue.aws_glue_job_sensor import AwsGlueJobSensorOperator
# from aws_glue.aws_glue_job_hook import AwsGlueJobHook


class AwsGluePlugin(AirflowPlugin):
    name = "aws_glue_plugin"
    operators = [AWSGlueJobOperator, AwsGlueJobSensorOperator]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
