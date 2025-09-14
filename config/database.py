from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv(".env")

db = PostgresqlDatabase(
    os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT"))
)
