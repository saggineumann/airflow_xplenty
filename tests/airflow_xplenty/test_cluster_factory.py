import unittest
from mock import MagicMock
from mock import Mock
from airflow_xplenty.cluster_factory import ClusterFactory

class ClusterFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.factory = ClusterFactory(self.client, 'test_env', poll_interval=0.001)

    def test_find_or_start_with_existing_available_cluster(self):
        cluster = Mock(type='test_env', status='available')
        self.client.clusters = [cluster]

        self.client.create_cluster = MagicMock()

        self.factory.find_or_start()
        self.assertEqual(len(self.client.create_cluster.mock_calls), 0)

    def test_find_or_start_with_existing_pending_cluster(self):
        cluster = Mock(id=42, type='test_env', status='pending')
        self.client.clusters = [cluster]

        updated_cluster = Mock(status='available')
        self.client.get_cluster = MagicMock(return_value=updated_cluster)

        self.factory.find_or_start()
        self.client.get_cluster.assert_called_once_with(42)

    def test_find_or_start_with_existing_terminating_cluster(self):
        cluster = Mock(id=42, type='test_env', status='terminating')
        self.client.clusters = [cluster]

        new_cluster = Mock(status='available')
        self.client.create_cluster = MagicMock(return_value=new_cluster)

        self.factory.find_or_start()
        self.client.create_cluster.assert_called_once_with('test_env', 1,
            'airflow-test_env-cluster', 'Cluster to run Airflow packages')

    def test_find_or_start_with_no_existing_cluster(self):
        self.client.clusters = []

        new_cluster = Mock(id=42, status='pending')
        self.client.create_cluster = MagicMock(return_value=new_cluster)

        updated_cluster = Mock(status='available')
        self.client.get_cluster = MagicMock(return_value=updated_cluster)

        self.factory.find_or_start()
        self.client.get_cluster.assert_called_once_with(42)

if __name__ == '__main__':
    unittest.main()
