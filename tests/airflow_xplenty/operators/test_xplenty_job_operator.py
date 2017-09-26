import unittest
from airflow.configuration import conf
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyJobOperator

class XplentyJobOperatorTestCase(unittest.TestCase):
    def mock_operator(self, operator):
        cluster = Mock(id=42)
        operator.cluster_factory.find_or_start = MagicMock(return_value=cluster)
        operator.job_manager.run = MagicMock()

    def setUp(self):
        # TODO: set these values in unittest.cfg and have Airflow read from there
        if not conf.has_section('xplenty'): conf.add_section('xplenty')
        conf.set('xplenty', 'account_id', 'TestAccount')
        conf.set('xplenty', 'api_key', 'TestKey')

    def test_no_package_id_or_name(self):
        self.assertRaises(TypeError, XplentyJobOperator, task_id='test')

    def test_both_package_id_and_name(self):
        self.assertRaises(TypeError, XplentyJobOperator, task_id='test',
            package_id=1, package_name='TestPackage')

    def test_execute_lazily_start_cluster(self):
        operator = XplentyJobOperator(package_name='test_package', task_id='test')
        self.mock_operator(operator)

        package = Mock(id=314)
        operator.package_finder.find = MagicMock(return_value=package)

        operator.execute({})
        operator.cluster_factory.find_or_start.assert_called_once_with()

    def test_execute_missing_package_id(self):
        operator = XplentyJobOperator(package_id='-1', task_id='test')
        self.mock_operator(operator)

        operator.client.get_package = MagicMock(return_value=None)
        self.assertRaises(Exception, operator.execute, {})

    def test_execute_missing_package_name(self):
        operator = XplentyJobOperator(package_name='test_package', task_id='test')
        self.mock_operator(operator)

        operator.package_finder.find = MagicMock(return_value=None)
        self.assertRaises(Exception, operator.execute, {})

    def test_execute_run_job(self):
        operator = XplentyJobOperator(package_name='test_package', task_id='test')
        self.mock_operator(operator)

        package = Mock(id=314)
        operator.package_finder.find = MagicMock(return_value=package)

        operator.execute({})
        operator.job_manager.run.assert_called_once_with(42, 314)

    def test_on_kill(self):
        operator = XplentyJobOperator(package_name='test_package', task_id='test')
        self.mock_operator(operator)
        operator.job_manager.stop = MagicMock()
        operator.on_kill()
        operator.job_manager.stop.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
