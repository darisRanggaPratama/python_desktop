import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'testing'
        self.user = 'rangga'
        self.password = 'rangga'
        self.port = 3306
    
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None