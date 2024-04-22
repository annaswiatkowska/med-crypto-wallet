import os
import psycopg2
from dotenv import load_dotenv

def connect():
    load_dotenv()
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST")
        )

    except Exception as e:
        print("Error:", e)

    return conn, conn.cursor()

def select(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def insert(cursor, query):
    try:
        cursor.execute(query)
        print('Insertion successful. Status message: ', cursor.statusmessage)
        cursor.execute("COMMIT;")
    except psycopg2.Error as e:
        print('Error: ', e)


def close_connection(conn, cursor):
    cursor.close()
    conn.close()

# TEST
if __name__ == "__main__":
    conn, cursor = connect()
    result = select(cursor, 'SELECT * FROM users;')
    print(result)
    close_connection(conn, cursor)