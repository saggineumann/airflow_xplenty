import os
from client_factory import ClientFactory

class Package:
    def __init__(self, name):
        self.client = ClientFactory().client()
        self.name = name

    def find(self):
        for package in self.client.packages:
            if package.name == self.name:
                return package
