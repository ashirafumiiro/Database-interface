import abc
import sqlite3

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


class SQLLiteDatabase(DatabaseInterface):
    """SQLLite database provider, implementing the database interface"""

    def __init__(self, db_url):
        self.conn = sqlite3.connect(db_url)

    def create(self, table_name: str, params: dict):
        query = "INSERT INTO " + table_name + " ("
        i = 1
        for key in params.keys():
            query += key
            if i < len(params):
                query += ","
                i += 1
        query += ") VALUES ("
        i = 1
        for key in params.keys():
            query += self.get_value(params[key])
            if i < len(params):
                query += ","
                i += 1
        query += ");"
        self.execute_query(query)
        self.conn.commit()

    def read(self, table: str, filter_params: dict):
        query = "SELECT * FROM " + table
        if len(filter_params) > 0:
            query += " WHERE "
            i = 1
            for key in filter_params.keys():
                query += "{}={}".format(key, self.get_value(filter_params[key]))
                if i < len(filter_params):
                    query += " AND "
                    i += 1
        self.conn.row_factory = sqlite3.Row
        cursor = self.execute_query(query)
        rows = []
        for row in cursor.fetchall():
            rows.append(dict(row))
        return rows

    def update(self, table: str, _id: int, params: dict):
        query = "UPDATE " + table + " SET"
        i = 1
        for key in params.keys():
            query += " {}={}".format(key, self.get_value(params[key]))
            if i < len(params):
                query += ", "
                i += 1
        query += " WHERE id="+str(_id)
        self.execute_query(query)
        self.conn.commit()

    def delete(self, table: str, filter_params: dict):
        """Delets an Entry based on a dictionary of filters"""
        query = "DELETE FROM " + table
        if len(filter_params) > 0:
            query += " WHERE "
            i = 1
            for key in filter_params.keys():
                query += "{}={}".format(key, self.get_value(filter_params[key]))
                if i < len(filter_params):
                    query += " AND "
                    i += 1
        self.execute_query(query)
        self.conn.commit()

    def execute_query(self, query: str):
        """Execute SQL query on the sqlite database"""
        try:
            return self.conn.execute(query)
        except AttributeError:
            print("No database Connected to")
        except sqlite3.OperationalError as ex:
            print(str(ex))

    def close(self):
        self.conn.close()

    @staticmethod
    def get_value(val) -> object:
        if isinstance(val, str):
            return "'{}'".format(val)
        else:
            return str(val)


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

