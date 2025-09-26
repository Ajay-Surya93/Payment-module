import psycopg2
from psycopg2 import OperationalError, Error

def connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="root@123",
            dbname="PaymentService"
        )
        print("Successfully connected to PostgreSQL")
        return connection
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None
    
    
def connection1():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="root@123",
            dbname="PaymentVerify"
        )
        print("Successfully connected to PostgreSQL")
        return connection
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

