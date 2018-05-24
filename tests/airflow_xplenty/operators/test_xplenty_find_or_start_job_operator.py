import unittest
from mock import MagicMock
from mock import Mock
from airflow_xplenty.operators import XplentyFindOrStartJobOperator


class XplentyFindOrStartJobOperatorTestCase(unittest.TestCase):
    def init_operator(
            self, package_id=None, package_name=None, variables_fn=None):
        self.operator = XplentyFindOrStartJobOperator(
            start_cluster_task_id='start_cluster', package_id=package_id,
            package_name=package_name, variables_fn=variables_fn,
            task_id='test')
        self.operator.client = Mock()
        self.operator.client.jobs = []

    def setUp(self):
        self.init_operator(package_id=24)
        self.task_instance = Mock()
        self.task_instance.xcom_pull = MagicMock(return_value=314)
        self.operator.client.add_job = MagicMock(return_value=Mock(id=9876))

    def test_init_no_package_info(self):
        with self.assertRaises(TypeError) as ctx:
            self.init_operator(package_id=None, package_name=None)
        self.assertEqual(
            '__init__ requires either package_id or package_name',
            str(ctx.exception))

    def test_init_package_id_and_name(self):
        with self.assertRaises(TypeError) as ctx:
            self.init_operator(package_id=24, package_name='do_stuff')
        self.assertEqual(
            'Do not supply both package_id and package_name',
            str(ctx.exception))

    def test_execute(self):
        return_value = self.operator.execute(
            {'task_instance': self.task_instance})
        self.assertEqual(9876, return_value)
        self.task_instance.xcom_pull.assert_called_with(
            task_ids='start_cluster')
        self.operator.client.add_job.assert_called_with(314, 24, {})

    def test_execute_with_package_name(self):
        self.init_operator(package_name='do_stuff')
        expected_package = Mock(id=24)
        expected_package.name = 'do_stuff'
        other_package = Mock(id=23)
        other_package.name = 'do_nada'
        packages = [other_package, expected_package]
        self.operator.client.get_packages = MagicMock(return_value=packages)
        self.operator.execute({'task_instance': self.task_instance})
        self.operator.client.add_job.assert_called_with(314, 24, {})

    def test_execute_with_package_name_fn(self):
        def package_name_fn(_context):
            return 'do_stuff_from_fn'

        self.init_operator(package_name=package_name_fn)
        expected_package = Mock(id=24)
        expected_package.name = 'do_stuff_from_fn'
        other_package = Mock(id=23)
        other_package.name = 'do_nada'
        packages = [other_package, expected_package]
        self.operator.client.get_packages = MagicMock(return_value=packages)
        self.operator.execute({'task_instance': self.task_instance})
        self.operator.client.add_job.assert_called_with(314, 24, {})

    def test_execute_with_invalid_package_name(self):
        self.init_operator(package_name='do_stuff')
        other_package = Mock(id=23)
        other_package.name = 'do_nada'
        packages = [other_package]
        self.operator.client.get_packages.side_effect = [
            MagicMock(return_value=packages), []]
        with self.assertRaises(Exception) as ctx:
            self.operator.execute({'task_instance': self.task_instance})
        self.assertEqual('Package do_stuff not found', str(ctx.exception))

    def test_execute_with_variables_fn(self):
        def variables_fn(_context):
            return {'a': 1, 'b': 2}
        self.init_operator(package_id=24, variables_fn=variables_fn)
        self.operator.execute({'task_instance': self.task_instance})
        self.operator.client.add_job.assert_called_with(
            314, 24, {'a': 1, 'b': 2})

    def test_execute_with_reuasable_job(self):
        self.operator.client.jobs = [
            Mock(id=5432, package_id=24, status='running')]
        return_value = self.operator.execute(
            {'task_instance': self.task_instance})
        self.assertEqual(5432, return_value)
        self.operator.client.add_job.assert_not_called()

    def test_execute_with_same_package_failed_job(self):
        self.operator.client.jobs = [
            Mock(id=5432, package_id=24, status='failed')]
        return_value = self.operator.execute(
            {'task_instance': self.task_instance})
        self.assertEqual(9876, return_value)
        self.operator.client.add_job.assert_called_with(314, 24, {})

    def test_execute_with_different_package_job(self):
        self.operator.client.jobs = [
            Mock(id=5432, package_id=99, status='running')]
        return_value = self.operator.execute(
            {'task_instance': self.task_instance})
        self.assertEqual(9876, return_value)
        self.operator.client.add_job.assert_called_with(314, 24, {})

    def test_execute_with_no_xcoms(self):
        self.task_instance.xcom_pull = MagicMock(return_value=None)
        with self.assertRaises(Exception) as ctx:
            self.operator.execute({'task_instance': self.task_instance})
        self.assertEqual('No cluster_id found in XComs', str(ctx.exception))
