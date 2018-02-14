import unittest
from airflow.configuration import conf
from airflow_xplenty.client_factory import ClientFactory, XplentyV2Client


class ClientFactoryTestCase(unittest.TestCase):
    def setUp(self):
        # TODO: set these values in unittest.cfg and have Airflow read from there
        if not conf.has_section('xplenty'): conf.add_section('xplenty')
        conf.set('xplenty', 'account_id', 'TestAccount')
        conf.set('xplenty', 'api_key', 'TestKey')

    def test_client_type(self):
        factory = ClientFactory()
        client = factory.client()
        self.assertEqual(type(client), XplentyV2Client)

    def test_client_account_id(self):
        factory = ClientFactory()
        client = factory.client()
        self.assertEqual(client.account_id, 'TestAccount')

    def test_client_api_key(self):
        factory = ClientFactory()
        client = factory.client()
        self.assertEqual(client.api_key, 'TestKey')


if __name__ == '__main__':
    unittest.main()
