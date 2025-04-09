import psycopg2
from config import DATABASE

conn = psycopg2.connect(DATABASE, sslmode="require")
cursor = conn.cursor()