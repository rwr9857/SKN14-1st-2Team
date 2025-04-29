import mysql.connector

# DB 연결
db_connection = mysql.connector.connect(
    host="localhost", user="root", password="mysql", database="teamdb"
)
