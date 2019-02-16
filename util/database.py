from config.config import ip_address, port
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = MongoClient(ip_address, port)

    def getClient(self):
        return self.client