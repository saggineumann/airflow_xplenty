import os
import unittest
from airflow_xplenty.client_factory import ClientFactory
from xplenty import XplentyClient

class ClientFactoryTestCase(unittest.TestCase):
    def test_constructor_default_account_id_without_env_var(self):
        self.assertRaises(Exception, ClientFactory, api_key='TestKey')

    def test_constructor_default_api_key_without_env_var(self):
        self.assertRaises(Exception, ClientFactory, account_id='TestAccount')

    def test_client_type(self):
        factory = ClientFactory(account_id='TestAccount', api_key='TestKey')
        client = factory.client()
        self.assertEqual(type(client), XplentyClient)

    def test_client_account_id(self):
        factory = ClientFactory(account_id='TestAccount', api_key='TestKey')
        client = factory.client()
        self.assertEqual(client.account_id, 'TestAccount')

    def test_client_default_account_id_with_env_var(self):
        os.environ['XPLENTY_ACCOUNT_ID'] = 'EnvAccount'
        factory = ClientFactory(api_key='TestKey')
        client = factory.client()
        self.assertEqual(client.account_id, 'EnvAccount')
        os.environ.pop('XPLENTY_ACCOUNT_ID', None)

    def test_client_api_key(self):
        factory = ClientFactory(account_id='TestAccount', api_key='TestKey')
        client = factory.client()
        self.assertEqual(client.api_key, 'TestKey')

    def test_client_default_api_key_with_env_var(self):
        os.environ['XPLENTY_API_KEY'] = 'EnvKey'
        factory = ClientFactory(account_id='TestAccount')
        client = factory.client()
        self.assertEqual(client.api_key, 'EnvKey')
        os.environ.pop('XPLENTY_API_KEY', None)

if __name__ == '__main__':
    unittest.main()
