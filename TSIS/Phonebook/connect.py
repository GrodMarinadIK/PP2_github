# connect.py
import psycopg2
from config import params

def get_connection():
    """Creates and returns object of connection with DB""" 
    try:
        # Unpacking dictionary params directly in arguments of function
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при подключении к PostgreSQL: {error}")
        return None