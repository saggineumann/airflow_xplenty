import unittest
from mock import MagicMock
from mock import Mock
from airflow_xplenty.job_manager import JobManager

class JobManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.manager = JobManager(self.client, poll_interval=0.001)

    def test_run_adds_job(self):
        job = Mock(id=42, status='completed', progress=1.0)
        self.client.add_job = MagicMock(return_value=job)

        self.manager.run(314, 999)
        self.client.add_job.assert_called_once_with(314, 999, {})

    def test_run_until_completed(self):
        job1 = Mock(id=42, status='running', progress=0.5)
        self.client.add_job = MagicMock(return_value=job1)

        job2 = Mock(status='completed', progress=1.0)
        self.client.get_job = MagicMock(return_value=job2)

        self.manager.run(314, 999)
        self.client.get_job.assert_called_once_with(42)

    def test_run_until_stopped(self):
        job1 = Mock(id=42, status='running', progress=0.5)
        self.client.add_job = MagicMock(return_value=job1)

        job2 = Mock(status='stopped', progress=1.0)
        self.client.get_job = MagicMock(return_value=job2)

        self.manager.run(314, 999)
        self.client.get_job.assert_called_once_with(42)

    def test_run_until_failed(self):
        job1 = Mock(id=42, status='running', progress=0.5)
        self.client.add_job = MagicMock(return_value=job1)

        job2 = Mock(status='failed', errors='Nooo!')
        self.client.get_job = MagicMock(return_value=job2)

        self.assertRaises(Exception, self.manager.run, 314, 999)

    def test_stop(self):
        self.manager.job_id = 42
        self.client.terminate_job = MagicMock()
        self.manager.stop()
        self.client.terminate_job.assert_called_once_with(42)

if __name__ == '__main__':
    unittest.main()
