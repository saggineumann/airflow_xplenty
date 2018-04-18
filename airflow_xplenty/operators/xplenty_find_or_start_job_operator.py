import json
import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow_xplenty.client_factory import ClientFactory

RUNNING_STATUSES = ['idle', 'pending', 'running']


def _find_package(client, name):
    offset = 0
    page_size = 100
    while True:
        packages = client.get_packages(offset=offset, limit=page_size)
        if not packages:
            return None

        for package in packages:
            if package.name == name:
                return package

        offset += page_size


class XplentyFindOrStartJobOperator(BaseOperator):
    """Operator start a job on an Xplenty cluster
    """
    @apply_defaults
    def __init__(self, start_cluster_task_id, package_id=None,
                 package_name=None, variables_fn=None, **kwargs):
        if package_id is None and package_name is None:
            raise TypeError(
                '__init__ requires either package_id or package_name')

        if package_id is not None and package_name is not None:
            raise TypeError('Do not supply both package_id and package_name')

        self.package_id = package_id
        self.package_name = package_name
        self.start_cluster_task_id = start_cluster_task_id
        self.client = ClientFactory().client()
        self.variables_fn = variables_fn

        super(XplentyFindOrStartJobOperator, self).__init__(**kwargs)

    def execute(self, context):
        cluster_id = context['task_instance'].xcom_pull(
            task_ids=self.start_cluster_task_id)
        if cluster_id is None:
            raise Exception('No cluster_id found in XComs')

        if self.package_name is not None:
            package = _find_package(self.client, self.package_name)
            if package is None:
                raise Exception('Package %s not found' % self.package_name)
            self.package_id = package.id

        # Only try to reuse existing running jobs when there are no variables.
        if self.variables_fn is None:
            for job in self.client.jobs:
                if self._is_reusable_job(job):
                    logging.info('Found already running job %d', job.id)
                    return job.id

        if self.variables_fn is None:
            variables = {}
        else:
            variables = self.variables_fn(context)

        job = self.client.add_job(cluster_id, self.package_id, variables)
        pretty_variables = json.dumps(variables, indent=4)
        logging.info(
            'Starting job %d with variables %s', job.id, pretty_variables)
        return job.id

    def _is_reusable_job(self, job):
        if job.package_id != self.package_id:
            return False

        return job.status in RUNNING_STATUSES
