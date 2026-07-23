"""
PostgreSQL Verbindung
"""

import os

import psycopg2

from modules.database.config import DB_CONFIG


class Database:

    def __init__(self):
        self.connection = None

    def connect(self):

        if self.connection and self.connection.closed == 0:
            return self.connection

        database_url = os.getenv("DATABASE_URL")

        if database_url:
            # Online, zum Beispiel Railway
            self.connection = psycopg2.connect(database_url)
        else:
            # Lokal auf deinem PC
            self.connection = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                dbname=DB_CONFIG["database"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
            )

        return self.connection

    def close(self):

        if self.connection:
            self.connection.close()
            self.connection = None