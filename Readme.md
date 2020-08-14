## Database interface implemented with singleton pattern and DI

In order to create a standard interface, all database providers subclass the Abstract class `DatabaseInterface` and must implement all the abstract methods required  
  
A factory `Database` that is used to create the database interaces is implemented using singleton implemntation pattern design.  
A SQLite Database provider has been implemented as a test example.   
The `main.py` file shows the sample usage of these classes with comments.