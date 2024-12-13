import mysql.connector
import pymysql

def connect_to_db():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="thuCung2"
    )
    return connection

db = connect_to_db()
cursor = db.cursor()

