import unittest
from airflow.configuration import conf
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyFindOrStartClusterOperator


class XplentyFindOrStartClusterOperatorTestCase(unittest.TestCase):
    def setUp(self):
        self.operator = XplentyFindOrStartClusterOperator(
            env='sandbox', task_id='test')
        cluster = Mock(id=42)
        self.operator.client.create_cluster = MagicMock(return_value=cluster)

    def test_execute_lazily_start_cluster(self):
        self.operator.client.get_clusters = MagicMock(return_value=[])
        self.operator.execute({})
        self.operator.client.create_cluster.assert_called_once_with(
            'sandbox', 1, 'airflow-sandbox-cluster',
            'Cluster to run Airflow packages')

    def test_execute_lazily_start_cluster_none_available(self):
        terminated_cluster = Mock(id=21, type='sandbox', status='terminated')
        get_cluster = Mock()
        get_cluster.side_effect = [[terminated_cluster], []]
        self.operator.client.get_clusters = get_cluster
        self.operator.execute({})
        self.operator.client.create_cluster.assert_called_once_with(
            'sandbox', 1, 'airflow-sandbox-cluster',
            'Cluster to run Airflow packages')

    def test_execute_lazily_start_cluster_wrong_env(self):
        terminated_cluster = Mock(id=21, type='production', status='available')
        get_cluster = Mock()
        get_cluster.side_effect = [[terminated_cluster], []]
        self.operator.client.get_clusters = get_cluster
        self.operator.execute({})
        self.operator.client.create_cluster.assert_called_once_with(
            'sandbox', 1, 'airflow-sandbox-cluster',
            'Cluster to run Airflow packages')

    def test_start_cluster_return_value(self):
        self.operator.client.get_clusters = MagicMock(return_value=[])
        self.assertEqual(self.operator.execute({}), 42)

    def test_find_available_cluster(self):
        available_cluster = Mock(id=21, type='sandbox', status='available')
        get_cluster = Mock()
        get_cluster.side_effect = [[available_cluster], []]
        self.operator.client.get_clusters = get_cluster
        self.assertEqual(self.operator.execute({}), 21)
