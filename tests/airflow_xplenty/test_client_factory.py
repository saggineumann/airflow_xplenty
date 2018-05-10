import unittest
from mock import MagicMock
from airflow.configuration import conf
from airflow_xplenty.client_factory import ClientFactory, XplentyV2Client
from xplenty import Job


class ClientFactoryTestCase(unittest.TestCase):
    def setUp(self):
        if not conf.has_section('xplenty'):
            conf.add_section('xplenty')
        conf.set('xplenty', 'account_id', 'TestAccount')
        conf.set('xplenty', 'api_key', 'TestKey')
        self.client = ClientFactory().client()

    def test_client_type(self):
        self.assertEqual(type(self.client), XplentyV2Client)

    def test_client_account_id(self):
        self.assertEqual(self.client.account_id, 'TestAccount')

    def test_client_api_key(self):
        self.assertEqual(self.client.api_key, 'TestKey')

    def test_get_job(self):
        self.client.get = MagicMock(return_value={'outputs': 'boom'})
        job = self.client.get_job(34)
        self.client.get.assert_called_with(
            'https://api.xplenty.com/TestAccount/api/jobs/34')
        self.assertEqual(Job, type(job))
        self.assertEqual('boom', job.outputs)
