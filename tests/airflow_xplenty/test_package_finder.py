import unittest
from mock import Mock
from mock import MagicMock
from airflow_xplenty.package_finder import PackageFinder

class PackageFinderTestCase(unittest.TestCase):
    package1 = Mock()
    package1.name = 'package1'
    package2 = Mock()
    package2.name = 'package2'

    def responses(self, offset, limit):
        if offset == 0 and limit == 100:
            return [self.package1]
        elif offset == 100 and limit == 100:
            return [self.package2]
        else:
            return []

    def setUp(self):
        self.client = Mock()
        self.client.get_packages = Mock(side_effect=self.responses)
        self.finder = PackageFinder(self.client)

    def test_find_with_existing_name(self):
        self.assertEqual(self.finder.find('package1'), self.package1)

    def test_find_with_existing_name_on_second_page(self):
        self.assertEqual(self.finder.find('package2'), self.package2)

    def test_find_with_missing_name(self):
        self.assertIsNone(self.finder.find('invalid_package'))

if __name__ == '__main__':
    unittest.main()
