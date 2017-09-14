import os
import time
from client_factory import ClientFactory

class XplentyJob:
    FINAL_STATUSES = ['completed', 'failed', 'stopped']

    def __init__(self, cluster_id, package_id):
        self.client = ClientFactory().client()
        self.cluster_id = cluster_id
        self.package_id = package_id
        self.job_id = None

    def run(self):
        job = self.client.add_job(self.cluster_id, self.package_id, {})
        self.job_id = job.id

        while job.status not in self.FINAL_STATUSES:
            time.sleep(10)
            job = self.client.get_job(self.job_id)

        if job.status == 'failed':
            raise Exception('Job for package_id %d failed: %s' % (self.package_id, job.errors))

    def stop(self):
        if self.job_id is not None:
            self.client.terminate_job(self.job_id)
