import unittest
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyWaitForJobSensor


class XplentyWaitForJobSensorTestCase(unittest.TestCase):
    def setUp(self):
        self.operator = XplentyWaitForJobSensor(
            start_job_task_id='start_job', task_id='test')
        self.task_instance = Mock()
        self.task_instance.xcom_pull = MagicMock(return_value=314)

    def stub_get_job(self, status, **kwargs):
        job = Mock(status=status, **kwargs)
        self.operator.client.get_job = MagicMock(return_value=job)

    def test_poke_with_running_job(self):
        self.stub_get_job(status='running', progress=0.5)
        poke = self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual(False, poke)
        self.task_instance.xcom_pull.assert_called_with(task_ids='start_job')
        self.operator.client.get_job.assert_called_once_with(314)

    def test_poke_with_completed_job(self):
        self.stub_get_job(status='completed', outputs='donezo!')
        self.task_instance.xcom_push = MagicMock()
        poke = self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual(True, poke)
        self.task_instance.xcom_push.assert_called_with(
            key='xplenty_job_outputs', value='donezo!')

    def test_poke_with_stopped_job(self):
        self.stub_get_job(status='stopped', errors='terminated!')
        with self.assertRaises(Exception) as ctx:
            self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual('Job failed: terminated!', str(ctx.exception))

    def test_poke_with_failed_job(self):
        self.stub_get_job(status='failed', errors='kaboom!')
        with self.assertRaises(Exception) as ctx:
            self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual('Job failed: kaboom!', str(ctx.exception))

    def test_poke_with_no_xcoms(self):
        self.task_instance.xcom_pull = MagicMock(return_value=None)
        with self.assertRaises(Exception) as ctx:
            self.operator.poke({'task_instance': self.task_instance})
        self.assertEqual('No job_id found in XComs', str(ctx.exception))
