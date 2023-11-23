import configparser
import pymongo
import logging

log = logging.getLogger(__name__)


class MongoManager:
    """
    Class to connect with mongo database and handle all operations related to.
    """
    def __init__(self, config_path='./config.ini'):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_path)
        self.client = pymongo.MongoClient(self.cfg.get('mongo', 'host'),
                                          self.cfg.getint('mongo', 'port'),
                                          username=self.cfg.get('mongo', 'username'),
                                          password=self.cfg.get('mongo', 'password'))
        self.db = self.client['eLibrary']

    @property
    def users_collection(self):
        return self.db['Users']
