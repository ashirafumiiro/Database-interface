import abc


instance = None


class DatabaseInterface(metaclass=abc.ABCMeta):
    """Database Interface"""

    @abc.abstractmethod
    def create(self, table_name: str, params: dict):
        pass

    @abc.abstractmethod
    def read(self, table: str, filter_params: dict):
        """updates an entry based on the id"""
        pass

    @abc.abstractmethod
    def update(self, table: str, _id: int, params: dict):
        pass

    @abc.abstractmethod
    def delete(self, table: str, filter_params: dict):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class Database:
    def __init__(self):
        """Initialising the interface"""
        self.provider = None
        global instance
        instance = self
        self.db_url = "db.sqlite"

    @staticmethod
    def get_instance(re_init=False):
        """get an instance of the Example class"""
        global instance
        if instance is None or re_init is True:
            return Database()
        return instance

    def set_provider(self, provider):
        """set provider"""
        self.provider = provider

    def create(self, table_name: str, params: dict):
        """perform action"""
        self.provider.create(table_name, params)

    def read(self, table: str, filter_params: dict):
        """Perform read operation"""
        return self.provider.read(table, filter_params)

    def update(self, table: str, _id: int, params: dict):
        """Perform the update operation based on the id"""
        self.provider.update(table, _id, params)

    def delete(self, table: str, filter_params: dict):
        """Perform the delete operation based on the filter_params"""
        self.provider.delete(table, filter_params)

