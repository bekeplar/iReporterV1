from os import environ

import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(environ.get("DATABASE_URL"))
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        except (Exception, psycopg2.Error) as e:
            print(e)
