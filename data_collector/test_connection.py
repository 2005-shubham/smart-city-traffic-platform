import psycopg2
from dotenv import load_dotenv
import os

# .env file se variables load karo
load_dotenv()

# Database se connect karne ki koshish karo
try:
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    print("Successfully connected to the database!")
    connection.close()
except Exception as e:
    print("Failed to connect to the database:", e)