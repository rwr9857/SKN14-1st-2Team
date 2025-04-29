import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                    charset=os.getenv("DB_CHARSET"),
                )
            except Error as e:
                print("DB 연결 실패:", e)
                cls._instance = None
        return cls._instance

    def get_connection(self):
        return self._connection

    def close(self):
        if self._connection.is_connected():
            self._connection.close()
            print("DB 연결 종료됨")
