import unittest
from mock import Mock
from airflow_xplenty.package_finder import PackageFinder

class PackageFinderTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.finder = PackageFinder(self.client)

    def test_find_with_existing_name(self):
        package = Mock()
        package.name = 'TestName'
        self.client.packages = [package]
        self.assertEqual(self.finder.find('TestName'), package)

    def test_find_with_missing_name(self):
        package = Mock()
        package.name = 'OtherName'
        self.client.packages = [package]
        self.assertIsNone(self.finder.find('TestName'))

if __name__ == '__main__':
    unittest.main()
