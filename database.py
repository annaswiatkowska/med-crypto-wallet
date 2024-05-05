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
        print("Error: ", e)

    return conn, conn.cursor()

# for data retrieval
def select(cursor, query):
    cursor.execute(query)
    result_list = cursor.fetchall()
    try:
        result = result_list[0][0]
    except:
        return None
    return result

# for record insertion or deletion
def update(cursor, query):
    try:
        cursor.execute(query)
        print("Successful update. Status message: ", cursor.statusmessage)
        cursor.execute("COMMIT;")
    except psycopg2.Error as e:
        print("Error: ", e)

def close_connection(conn, cursor):
    cursor.close()
    conn.close()
