import mysql.connector
from .database_utils import load_sql_file

config = {
    'user' : 'root',
    'password' : '',
    'host' : '127.0.0.1',
}

class CreateDatabase():
    def __init__(self,db_config):
        self.database_name = "gorillamind_telegram"
        self.connection = mysql.connector.connect(**db_config)
        if self.database_exists():
            self.use_this_database()
        else:
            self.create_database()
            self.use_this_database()
            self.create_tables()

    def create_database(self):
        self.execute_commands("CREATE DATABASE {database_name}".format(database_name=self.database_name))

    def database_exists(self):
        existing_databases = self.execute_queries("SHOW DATABASES")
        database_tuple = (self.database_name,)
        return database_tuple in existing_databases
    
    def create_tables(self):
        cursor = self.connection.cursor()
        for command in load_sql_file("create_tables.sql"):
            cursor.execute(command)
        self.connection.commit()
        cursor.close()

    def use_this_database(self):
        self.execute_commands("USE {database_name}".format(database_name=self.database_name))

    def execute_commands(self,command,params=(),multi=False):
        cursor = self.connection.cursor()
        cursor.execute(command,params,multi)
        self.connection.commit()
        cursor.close()

    def execute_queries(self,commands,params=(),multi=False):
        cursor = self.connection.cursor()
        cursor.execute(commands,params,multi)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
# Creates SQL Database, stored in mySQL server
mydb = CreateDatabase(config)

