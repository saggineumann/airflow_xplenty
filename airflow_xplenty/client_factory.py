import os
from airflow import configuration
from xplenty import XplentyClient

class ClientFactory:
    def __init__(self):
        self.account_id = configuration.get('xplenty', 'account_id')
        self.api_key = configuration.get('xplenty', 'api_key')

    def client(self):
        return XplentyClient(self.account_id, self.api_key)
