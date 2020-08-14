from Database import Database
from SQLiteDb import SQLiteDatabase

if __name__ == '__main__':
    drop_existing_table = "DROP TABLE IF EXISTS COMPANY;"
    sql_table_aquery = '''CREATE TABLE COMPANY
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME           TEXT    NOT NULL,
                 AGE            INT     NOT NULL,
                 ADDRESS        CHAR(50),
                 SALARY         REAL);'''
    sample_data1 = {"NAME": "Miiro", "AGE": 34, "ADDRESS": "KAWEMPE", "SALARY": 10000000}
    sample_data2 = {"NAME": "Ashiraf", "AGE": 34, "ADDRESS": "KAGOMA", "SALARY": 10000000}
    sample_table = "COMPANY"

    # Create provider and initialize it
    sqlite_provider = SQLiteDatabase("testDB.sqlite")
    sqlite_provider.execute_query(drop_existing_table)
    sqlite_provider.execute_query(sql_table_aquery)

    # get the singleton instance
    db = Database.get_instance()
    # attach the provider
    db.set_provider(sqlite_provider)

    print("Create and Read.............")
    # Create two entries
    db.create(sample_table, sample_data1)
    db.create(sample_table, sample_data2)

    # read Data
    data = db.read(sample_table, {})  # read all
    for row in data:
        print(row)

    # update first entry for with new addres and age
    db.update(sample_table, 1, {"AGE": 25, "ADDRESS": "NTINDA"})
    print("\nUpdated.......................")
    # read Data
    data = db.read(sample_table, {})  # read all
    for row in data:
        print(row)

    # Deleting data
    print("Delete second one............")
    db.delete(sample_table, sample_data2)
    # read Data
    data = db.read(sample_table, {})  # read all
    for row in data:
        print(row)
