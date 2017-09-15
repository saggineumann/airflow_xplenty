import time
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow_xplenty.client_factory import ClientFactory
from airflow_xplenty.cluster_factory import ClusterFactory
from airflow_xplenty.job_manager import JobManager
from airflow_xplenty.package_finder import PackageFinder

class XplentyJobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, package_name, env='sandbox', **kwargs):
        self.client = ClientFactory().client()
        self.env = env
        self.cluster_factory = ClusterFactory(self.client, self.env)
        self.package_finder = PackageFinder(self.client)
        self.job_manager = JobManager(self.client)
        self.package_name = package_name
        self.job = None

        super(XplentyJobOperator, self).__init__(**kwargs)

    def execute(self, context):
        cluster = self.cluster_factory.find_or_start()
        package = self.package_finder.find(self.package_name)

        if package is None:
            raise Exception('Package %s not found' % self.package_name)

        self.job_manager.run(cluster.id, package.id)

    def on_kill(self):
        self.job_manager.stop()
