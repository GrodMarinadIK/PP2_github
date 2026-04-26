# connect.py
import psycopg2
from config import params

def get_connection():
    """Creates and returns a psycopg2 connection to the DB."""
    try:
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"[ERROR] PostgreSQL connection failed: {error}")
        return None
    
    
