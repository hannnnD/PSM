import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="thuCung2"
    )

db = connect_to_db()
cursor = db.cursor()
