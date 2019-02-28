import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import runtime_mode
import os


class DatabaseConnection:
    def __init__(self):
        """class initializing method"""
        try:
            self.database_name = ""
            self.database_connect = None

            if runtime_mode == "Development":
                self.database_connect = self.database_connection("postgres")

            if runtime_mode == "Testing":
                self.database_connect = self.database_connection("testing_db")

            if runtime_mode == "Production":
                DATABASE_URL = os.environ['DATABASE_URL']
                self.database_connect = psycopg2.connect(DATABASE_URL, sslmode='require')

            self.database_connect.autocommit = True
            self.cursor_database = self.database_connect.cursor(cursor_factory=RealDictCursor)
            print('Connected to the database successfully.')
            
            create_user_table = """CREATE TABLE IF NOT EXISTS users
            (
                user_id SERIAL NOT NULL PRIMARY KEY,
                first_name VARCHAR(25) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                other_names VARCHAR(25) NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone_number VARCHAR(10) NOT NULL UNIQUE,
                user_name VARCHAR(50) NOT NULL UNIQUE,
                registered_on DATE DEFAULT CURRENT_TIMESTAMP,
                user_password VARCHAR(255) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE
            );"""

            create_incidents_table = """CREATE TABLE IF NOT EXISTS incidents
            (
                incident_id SERIAL NOT NULL PRIMARY KEY,
                title VARCHAR(125) NOT NULL,
                comment TEXT NOT NULL,
                location VARCHAR(50) NOT NULL,
                created_by INT NOT NULL,
                created_on  DATE DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) NOT NULL,
                incident_type VARCHAR(50) NOT NULL
            );"""

            create_auth_table = """CREATE TABLE IF NOT EXISTS users_auth
            (
                user_id SERIAL NOT NULL PRIMARY KEY,
                token VARCHAR(255) NOT NULL,
                is_blacklisted BOOLEAN DEFAULT FALSE,
                last_login DATE DEFAULT CURRENT_TIMESTAMP
            );"""

            create_images_db = """CREATE TABLE IF NOT EXISTS incident_images(
            incident_id SERIAL PRIMARY KEY,
            image_url VARCHAR(50)
            );"""

            create_videos_db = """CREATE TABLE IF NOT EXISTS incident_videos(
            incident_id SERIAL PRIMARY KEY,
            video_url VARCHAR(50) DEFAULT ''
            );"""

            self.cursor_database.execute(create_user_table)
            self.cursor_database.execute(create_auth_table)
            self.cursor_database.execute(create_incidents_table)
            self.cursor_database.execute(create_images_db)
            self.cursor_database.execute(create_videos_db)

        except (Exception, psycopg2.Error) as e:
            print(e)
    
    def database_connection(self, database_name):
            """Function for connecting to appropriate database"""
            return psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='bekeplar')

        
    def drop_table(self, table_name):
            """
            Drop tables after tests
            """
            drop = f"DROP TABLE {table_name} CASCADE;"
            self.cursor_database.execute(drop)


if __name__ == '__main__':
    database_name = DatabaseConnection()
