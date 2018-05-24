import unittest
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyWaitForClusterSensor


class XplentyWaitForClusterSensorTestCase(unittest.TestCase):
    def setUp(self):
        self.operator = XplentyWaitForClusterSensor(
            start_cluster_task_id='start_cluster', task_id='test')
        self.task_instance = Mock()
        self.task_instance.xcom_pull = MagicMock(return_value=314)

    def stub_get_cluster(self, status):
        cluster = Mock(status=status, id=314)
        self.operator.client.get_cluster = MagicMock(return_value=cluster)

    def test_poke_with_available_cluster(self):
        self.stub_get_cluster(status='available')
        poke = self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual(True, poke)
        self.task_instance.xcom_pull.assert_called_with(
            task_ids='start_cluster')
        self.operator.client.get_cluster.assert_called_once_with(314)

    def test_poke_with_creating_cluster(self):
        self.stub_get_cluster(status='creating')
        poke = self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual(False, poke)

    def test_poke_with_terminated_cluster(self):
        self.stub_get_cluster(status='terminated')
        with self.assertRaises(Exception) as ctx:
            self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual(
            'Cluster failed to start, in status: terminated',
            str(ctx.exception))

    def test_poke_with_no_xcoms(self):
        self.task_instance.xcom_pull = MagicMock(return_value=None)
        with self.assertRaises(Exception) as ctx:
            self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual('No cluster_id found in XComs', str(ctx.exception))
