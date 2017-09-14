import time
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow_xplenty.cluster import Cluster
from airflow_xplenty.job import Job
from airflow_xplenty.package import Package

class XplentyJobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, package_name, **kwargs):
        self.package_name = package_name
        self.job_id = None

        super(XplentyJobOperator, self).__init__(**kwargs)

    def execute(self, context):
        cluster = Cluster().find_or_start()
        package = Package(self.package_name).find()

        if package is None:
            raise Exception('Package %s not found' % self.package_name)

        self.job = Job(cluster.id, package.id)
        self.job.run()

    def on_kill(self):
        if self.job is not None:
            self.job.stop()
