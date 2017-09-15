import unittest
from airflow.configuration import conf
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyJobOperator

class XplentyJobOperatorTestCase(unittest.TestCase):
    def setUp(self):
        if not conf.has_section('xplenty'): conf.add_section('xplenty')
        conf.set('xplenty', 'account_id', 'TestAccount')
        conf.set('xplenty', 'api_key', 'TestKey')

        self.operator = XplentyJobOperator(package_name='test_package', task_id='test')

        cluster = Mock(id=42)
        self.operator.cluster_factory.find_or_start = MagicMock(return_value=cluster)

        package = Mock(id=314)
        self.operator.package_finder.find = MagicMock(return_value=package)

        self.operator.job_manager.run = MagicMock()

    def test_execute_lazily_start_cluster(self):
        self.operator.execute({})
        self.operator.cluster_factory.find_or_start.assert_called_once_with()

    def test_execute_missing_package(self):
        self.operator.package_finder.find = MagicMock(return_value=None)
        self.assertRaises(Exception, self.operator.execute, {})

    def test_execute_run_job(self):
        self.operator.execute({})
        self.operator.job_manager.run.assert_called_once_with(42, 314)

    def test_on_kill(self):
        self.operator.job_manager.stop = MagicMock()
        self.operator.on_kill()
        self.operator.job_manager.stop.assert_called_once_with()
