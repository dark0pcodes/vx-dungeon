from pymongo import MongoClient

from app.core.utils import load_config


class MongoCtrl:
    connection = None
    database = None

    def __new__(cls, *args, **kwargs):
        """
        Limit MONGO instances number to only one
        """
        if not hasattr(cls, 'instance'):
            mongo_cfg = load_config()['MONGO']
            cls.mongo_uri = f'mongodb://{mongo_cfg["USERNAME"]}:{mongo_cfg["PASSWORD"]}@{mongo_cfg["HOST"]}:' \
                            f'{mongo_cfg["PORT"]}/{mongo_cfg["DATABASE"]}'
            cls.database = mongo_cfg["DATABASE"]
            cls.instance = object.__new__(cls)
        return cls.instance

    def connect(self):
        """
        Start MongoDB
        Returns:
        """
        self.connection = MongoClient(self.mongo_uri)
        self.database = self.connection[self.database]


class Storage:
    def __init__(self, collection: str):
        self.collection = collection

    def __get_collection(self):
        """
        Resolve mongo collection
        Returns:
        """
        return MongoCtrl().database[self.collection]

    def query_one(self, *args, **kwargs):
        """
        Search single result
        Args:
            *args:
            **kwargs:

        Returns:

        """
        return self.__get_collection().find_one(*args, **kwargs)

    def query(self, *args, **kwargs):
        """
        Search multiple results
        Args:
            *args:
            **kwargs:

        Returns:

        """
        return self.__get_collection().find(*args, **kwargs)

    def save_one(self, *args, **kwargs):
        """
        Save a document in DB
        Args:
            *args:
            **kwargs:

        Returns:

        """
        return self.__get_collection().insert_one(*args, **kwargs)
