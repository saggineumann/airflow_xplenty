import os
from xplenty import XplentyClient

class ClientFactory:
    def __init__(self, account_id=None, api_key=None):
        if account_id is None:
            if 'XPLENTY_ACCOUNT_ID' not in os.environ:
                raise Exception('XPLENTY_ACCOUNT_ID environment variable must be set')
            else:
                account_id = os.environ['XPLENTY_ACCOUNT_ID']

        if api_key is None:
            if 'XPLENTY_API_KEY' not in os.environ:
                raise Exception('XPLENTY_API_KEY environment variable must be set')
            else:
                api_key = os.environ['XPLENTY_API_KEY']

        self.account_id = account_id
        self.api_key = api_key

    def client(self):
        return XplentyClient(self.account_id, self.api_key)
