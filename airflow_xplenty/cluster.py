import os
import time
from client_factory import ClientFactory

class Cluster:
    TERMINATING_STATUSES = ['pending_terminate', 'terminating', 'terminated', 'error']

    if 'XPLENTY_PRODUCITON_CLUSTER' in os.environ and os.environ['XPLENTY_PRODUCITON_CLUSTER'] == 'true':
        env = 'production'
    else:
        env = 'sandbox'

    def __init__(self, nodes=1):
        self.client = ClientFactory().client()
        self.nodes = nodes

    def terminate(self):
        for cluster in self.client.clusters:
            if cluster.name == self.name:
                self.client.terminate_cluster(cluster.id)
                break

    def find_or_start(self):
        cluster = self.find() or self.start()

        while cluster.status not in ['available'] + self.TERMINATING_STATUSES:
            time.sleep(10)
            cluster = self.client.get_cluster(cluster.id)

        if cluster.status != 'available':
            raise Exception('Error starting cluster: %s' % cluster.status)

        return cluster

    def find(self):
        for cluster in self.client.clusters:
            if cluster.type == self.env and cluster.status not in self.TERMINATING_STATUSES:
                return cluster

    def start(self):
        return self.client.create_cluster(self.env, self.nodes, 'airflow-cluster',
            'Cluster to run Airflow packages')
