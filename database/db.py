from os import environ
from flask import current_app as app
from urllib.parse import urlparse
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, Database_url):
        Database_url = "DATABASE_URL"
        #parsed_url = urlparse(Database_url)
        # db = parsed_url.path[1:]
        # username = parsed_url.username
        # hostname = parsed_url.hostname
        # password = parsed_url.password
        # port = parsed_url.port
        
        try:
            self.conn = psycopg2.connect(database='postgres', user='postgres',
                                    password='bekeplar', host='localhost',
                                    port=5432)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

            
            create_user_table = """CREATE TABLE IF NOT EXISTS users
            (
                id SERIAL NOT NULL PRIMARY KEY,
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
                id SERIAL NOT NULL PRIMARY KEY,
                title VARCHAR(125) NOT NULL,
                comment TEXT NOT NULL,
                location VARCHAR(50) NOT NULL,
                created_by uuid,
                created_on  DATE DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) NOT NULL,
                incident_type VARCHAR(50) NOT NULL
            );"""

            
            create_images_db = """CREATE TABLE IF NOT EXISTS incident_images(
            id SERIAL PRIMARY KEY,
            image_url VARCHAR(50),
            incident_id uuid
            );"""

            create_videos_db = """CREATE TABLE IF NOT EXISTS incident_videos(
            id SERIAL PRIMARY KEY,
            video_url VARCHAR(50) DEFAULT '',
            incident_id uuid
            );"""

            self.cursor.execute(create_user_table)
            self.cursor.execute(create_incidents_table)
            self.cursor.execute(create_images_db)
            self.cursor.execute(create_videos_db)


        except (Exception, psycopg2.Error) as e:
            print(e)

    def Database():
        database_obj = DatabaseConnection(app.config['DATABASE_URI'])
        return database_obj
