import unittest
from airflow.configuration import conf
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyFindOrStartClusterOperator

class XplentyFindOrStartClusterOperatorTestCase(unittest.TestCase):
    def test_execute_lazily_start_cluster(self):
        operator = XplentyFindOrStartClusterOperator(env='sandbox', task_id='test')
        cluster = Mock(id=42)
        operator.client.create_cluster = MagicMock(return_value=cluster)
        operator.client.get_clusters = MagicMock(return_value=[])
        operator.execute({})
        operator.client.create_cluster.assert_called_once_with('sandbox', 1,
            'airflow-sandbox-cluster', 'Cluster to run Airflow packages')

    def test_execute_lazily_start_cluster_none_available(self):
        operator = XplentyFindOrStartClusterOperator(env='sandbox', task_id='test')
        cluster = Mock(id=42)
        operator.client.create_cluster = MagicMock(return_value=cluster)
        terminated_cluster = Mock(id=21, type='sandbox', status='terminated')
        get_cluster = Mock()
        get_cluster.side_effect = [[terminated_cluster], []]
        operator.client.get_clusters = get_cluster
        operator.execute({})
        operator.client.create_cluster.assert_called_once_with('sandbox', 1,
            'airflow-sandbox-cluster', 'Cluster to run Airflow packages')

    def test_execute_lazily_start_cluster_wrong_env(self):
        operator = XplentyFindOrStartClusterOperator(env='sandbox', task_id='test')
        cluster = Mock(id=42)
        operator.client.create_cluster = MagicMock(return_value=cluster)
        terminated_cluster = Mock(id=21, type='production', status='available')
        get_cluster = Mock()
        get_cluster.side_effect = [[terminated_cluster], []]
        operator.client.get_clusters = get_cluster
        operator.execute({})
        operator.client.create_cluster.assert_called_once_with('sandbox', 1,
            'airflow-sandbox-cluster', 'Cluster to run Airflow packages')

    def test_start_cluster_return_value(self):
        operator = XplentyFindOrStartClusterOperator(env='sandbox', task_id='test')
        cluster = Mock(id=42)
        operator.client.create_cluster = MagicMock(return_value=cluster)
        operator.client.get_clusters = MagicMock(return_value=[])
        self.assertEqual(operator.execute({}), 42)

    def test_find_available_cluster(self):
        operator = XplentyFindOrStartClusterOperator(env='sandbox', task_id='test')
        terminated_cluster = Mock(id=21, type='sandbox', status='available')
        get_cluster = Mock()
        get_cluster.side_effect = [[terminated_cluster], []]
        operator.client.get_clusters = get_cluster
        self.assertEqual(operator.execute({}), 21)

if __name__ == '__main__':
    unittest.main()
