import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="kodkod", database="bulls_cows")

def init_db():
    connector = get_connection()
    try:
        cursor = connector.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games(  
        id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        secret_code VARCHAR(100) NOT NULL,
        attempts_used INT NOT NULL DEFAULT 0,
        status VARCHAR(50) NOT NULL DEFAULT 'in_progress'
        )
        """)
    finally:
            connector.close()