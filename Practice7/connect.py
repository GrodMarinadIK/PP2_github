# connect.py
import psycopg2
from config import params

def get_connection():
    """Создает и возвращает объект соединения с БД"""
    try:
        # Распаковываем словарь params прямо в аргументы функции
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при подключении к PostgreSQL: {error}")
        return None