import unittest
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyTerminateJobOperator


class XplentyTerminateJobOperatorTestCase(unittest.TestCase):
    def setUp(self):
        self.operator = XplentyTerminateJobOperator(
            start_job_task_id='start_job', task_id='test')
        self.operator.client.stop_job = MagicMock()

    def test_execute(self):
        task_instance = Mock()
        task_instance.xcom_pull = MagicMock(return_value=314)
        self.operator.execute({'task_instance': task_instance})
        task_instance.xcom_pull.assert_called_with(task_ids='start_job')
        self.operator.client.stop_job.assert_called_once_with(314)
